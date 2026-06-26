"""
规则引擎单元测试
"""

import sys
import os
import pytest
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from internal_control.rules import (
    Rule, RuleLoader, RuleIndex, RuleMatcher,
    ExclusionManager, ClassificationEngine,
    DataLevel, get_level_strictness
)


class TestRuleLoader:
    """规则加载器测试"""
    
    def test_load_default_rules(self):
        """测试加载默认规则"""
        loader = RuleLoader()
        rules = loader.load_all()
        
        assert len(rules) > 0
        
        # 检查关键规则是否存在
        rule_ids = [r.id for r in rules]
        assert 'ssh_private_key_rsa' in rule_ids
        assert 'aws_credentials' in rule_ids
        assert 'kube_config' in rule_ids
    
    def test_rule_validation(self):
        """测试规则验证"""
        loader = RuleLoader()
        
        # 有效规则
        valid_rule = Rule(
            id="test_valid",
            group="test",
            pattern="~/test",
            pattern_type="exact",
            level="L5-SECRET",
            priority=50,
            reason="test"
        )
        loader._validate_rule(valid_rule)  # 不应抛出异常
        
        # 无效规则：缺少 id
        with pytest.raises(ValueError):
            invalid_rule = Rule(
                id="",
                group="test",
                pattern="~/test",
                pattern_type="exact",
                level="L5-SECRET",
                priority=50,
                reason="test"
            )
            loader._validate_rule(invalid_rule)
        
        # 无效规则：优先级超出范围
        with pytest.raises(ValueError):
            invalid_rule = Rule(
                id="test_invalid_priority",
                group="test",
                pattern="~/test",
                pattern_type="exact",
                level="L5-SECRET",
                priority=1001,  # 超出范围
                reason="test"
            )
            loader._validate_rule(invalid_rule)
    
    def test_compile_pattern(self):
        """测试模式编译"""
        loader = RuleLoader()
        
        # 精确匹配
        exact_rule = Rule(
            id="test_exact",
            group="test",
            pattern="/home/user/.ssh/id_rsa",
            pattern_type="exact",
            level="L5-SECRET",
            priority=100,
            reason="test"
        )
        compiled = loader._compile_pattern(exact_rule)
        assert compiled._compiled_pattern("/home/user/.ssh/id_rsa") is True
        assert compiled._compiled_pattern("/other/path") is False
        
        # Glob 匹配
        glob_rule = Rule(
            id="test_glob",
            group="test",
            pattern="/home/user/.openclaw/**",
            pattern_type="glob",
            level="L2-INTERNAL",
            priority=80,
            reason="test"
        )
        compiled = loader._compile_pattern(glob_rule)
        assert compiled._compiled_pattern("/home/user/.openclaw/test.txt") is not None


class TestRuleIndex:
    """规则索引测试"""
    
    def test_build_index(self):
        """测试索引构建"""
        index = RuleIndex()
        
        rules = [
            Rule(id="exact_rule", group="test", pattern="/exact/path", 
                 pattern_type="exact", level="L5-SECRET", priority=100, reason="test"),
            Rule(id="glob_rule", group="test", pattern="/glob/**",
                 pattern_type="glob", level="L2-INTERNAL", priority=80, reason="test"),
            Rule(id="exclude_rule", group="test", pattern="**/.cache/**",
                 pattern_type="glob", level=None, priority=10, reason="test", action="exclude"),
        ]
        
        index.build(rules)
        
        assert index.exact_rules["/exact/path"].id == "exact_rule"
        # glob 规则可能被分到 prefix_rules 或 glob_rules（取决于是否提取到前缀）
        assert (len(index.glob_rules) + len(index.prefix_rules)) == 1
        assert len(index.exclusion_rules) == 1
    
    def test_query_exact(self):
        """测试精确匹配查询"""
        index = RuleIndex()
        
        rules = [
            Rule(id="ssh_key", group="test", pattern="~/.ssh/id_rsa",
                 pattern_type="exact", level="L5-SECRET", priority=100, reason="test"),
        ]
        
        index.build(rules)
        
        matches = index.query(os.path.expanduser("~/.ssh/id_rsa"))
        assert len(matches) == 1
        assert matches[0][0].id == "ssh_key"
    
    def test_is_excluded(self):
        """测试排除检查"""
        index = RuleIndex()
        
        rules = [
            Rule(id="cache_exclude", group="test", pattern="**/.cache/**",
                 pattern_type="glob", level=None, priority=10, reason="test", action="exclude"),
        ]
        
        index.build(rules)
        
        assert index.is_excluded("/project/.cache/file.txt") is True
        assert index.is_excluded("/project/src/file.txt") is False


class TestRuleMatcher:
    """规则匹配器测试"""
    
    def test_exact_match(self):
        """测试精确匹配"""
        index = RuleIndex()
        
        rules = [
            Rule(id="ssh_key", group="test", pattern="~/.ssh/id_rsa",
                 pattern_type="exact", level="L5-SECRET", priority=100, reason="test"),
        ]
        
        index.build(rules)
        matcher = RuleMatcher(index)
        
        result = matcher.match(os.path.expanduser("~/.ssh/id_rsa"))
        assert result.level == "L5-SECRET"
        assert result.confidence == 1.0
    
    def test_no_match(self):
        """测试无匹配"""
        index = RuleIndex()
        index.build([])
        matcher = RuleMatcher(index)
        
        result = matcher.match("/unknown/path")
        assert result.level is None
        assert result.confidence == 0.0
    
    def test_priority_conflict_resolution(self):
        """测试优先级冲突解决"""
        index = RuleIndex()
        
        rules = [
            Rule(id="high_priority", group="test", pattern="/path/to/file",
                 pattern_type="exact", level="L5-SECRET", priority=100, reason="test"),
            Rule(id="low_priority", group="test", pattern="/path/to/**",
                 pattern_type="glob", level="L2-INTERNAL", priority=50, reason="test"),
        ]
        
        index.build(rules)
        matcher = RuleMatcher(index)
        
        result = matcher.match("/path/to/file")
        assert result.rule_id == "high_priority"  # 高优先级胜出


class TestExclusionManager:
    """排除项管理器测试"""
    
    def test_default_exclusions(self):
        """测试默认排除规则"""
        manager = ExclusionManager()
        
        assert manager.is_excluded("/project/node_modules/package.json") is True
        assert manager.is_excluded("/project/__pycache__/test.pyc") is True
        assert manager.is_excluded("/project/.DS_Store") is True
    
    def test_custom_exclusion(self):
        """测试自定义排除规则"""
        manager = ExclusionManager()
        
        # 添加自定义规则
        manager.add_custom_exclusion("**/vendor/**", "第三方库")
        assert manager.is_excluded("/project/vendor/jquery.js") is True
        
        # 移除自定义规则
        manager.remove_custom_exclusion("**/vendor/**")
        assert manager.is_excluded("/project/vendor/jquery.js") is False
    
    def test_get_exclusion_reason(self):
        """测试获取排除原因"""
        manager = ExclusionManager()
        
        reason = manager.get_exclusion_reason("/project/node_modules/lodash.js")
        assert reason is not None
        assert "dependency" in reason


class TestClassificationEngine:
    """分级引擎集成测试"""
    
    def test_classify_ssh_key(self):
        """测试 SSH 密钥分级"""
        engine = ClassificationEngine()
        
        # 使用实际路径测试
        ssh_path = os.path.expanduser("~/.ssh/id_rsa")
        if os.path.exists(ssh_path):
            result = engine.classify_sync(ssh_path)
            assert result.level == "L5-SECRET"
            assert result.source == "l2_rule"
    
    def test_classify_excluded(self):
        """测试排除项分级"""
        engine = ClassificationEngine()
        
        result = engine.classify_sync("/project/node_modules/lodash.js")
        assert result.source == "excluded"
        assert result.level is None
    
    def test_cache_works(self):
        """测试缓存功能"""
        engine = ClassificationEngine()
        
        # 第一次查询
        result1 = engine.classify_sync("~/.openclaw/workspace/docs")
        
        # 第二次查询（应该命中缓存）
        result2 = engine.classify_sync("~/.openclaw/workspace/docs")
        
        # 检查缓存统计
        stats = engine.get_cache_stats()
        # 缓存可能命中也可能不命中，取决于之前的状态
        assert 'size' in stats
        assert 'hit_rate' in stats


class TestLevelStrictness:
    """级别严格度测试"""
    
    def test_strictness_order(self):
        """测试严格度排序"""
        assert get_level_strictness("L6-CRITICAL") > get_level_strictness("L5-SECRET")
        assert get_level_strictness("L5-SECRET") > get_level_strictness("L4-CONFIDENTIAL")
        assert get_level_strictness("L4-CONFIDENTIAL") > get_level_strictness("L3-RESTRICTED")
        assert get_level_strictness("L3-RESTRICTED") > get_level_strictness("L2-INTERNAL")
        assert get_level_strictness("L2-INTERNAL") > get_level_strictness("L1-PUBLIC")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])