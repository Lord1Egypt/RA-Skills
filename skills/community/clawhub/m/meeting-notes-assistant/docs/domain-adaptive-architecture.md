# 领域自适应识别架构设计文档

## 架构概述

本文档定义了 `meeting-notes-assistant` 的领域自适应识别架构，使其能够像通用 AI 一样支持所有行业和场景。

---

## 🏗️ 三层架构

```
┌─────────────────────────────────────────────────────────┐
│                  Layer 3: 领域自适应层                   │
│  • 自动领域检测                                          │
│  • 混合领域支持                                          │
│  • 用户自定义词典                                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│               Layer 2: 领域词典增强层                    │
│  • 多领域专业术语词典                                    │
│  • 自动术语修正                                          │
│  • 后处理规则引擎                                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              Layer 1: 基础转写层（已有）                  │
│  • Whisper large-v3 模型                                 │
│  • 多语言支持（99 种语言）                               │
│  • 通用识别率 70-90%                                    │
└─────────────────────────────────────────────────────────┘
```

---

## Layer 1: 基础转写层

### 功能
- 使用 Whisper large-v3 作为核心转写引擎
- 支持 99 种语言自动识别
- 通用识别率 70-90%（取决于领域）

### API 设计
```python
# scripts/base_transcriber.py

class BaseTranscriber:
    """基础转写器"""
    
    def __init__(self, model_size: str = "large-v3", device: str = "cuda"):
        self.model = whisper.load_model(model_size, device=device)
        self.device = device
    
    def transcribe(self, audio_path: str, language: str = None) -> Dict:
        """
        基础转写
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码（可选，None 表示自动检测）
        
        Returns:
            {
                "text": "转写文本",
                "language": "zh",
                "segments": [...],
                "duration": 3540.0
            }
        """
        result = self.model.transcribe(
            audio_path,
            language=language,
            fp16=False,
            verbose=False
        )
        return result
```

---

## Layer 2: 领域词典增强层

### 2.1 词典目录结构
```
domain-dictionaries/
├── general.json              # 通用词（默认）
├── finance.json              # 金融领域
├── healthcare.json           # 医疗领域
├── legal.json                # 法律领域
├── technology.json           # 技术领域
├── education.json            # 教育领域
├── manufacturing.json         # 制造业
├── retail.json               # 零售业
└── government.json            # 政务
```

### 2.2 词典数据结构
```json
{
  "domain": "finance",
  "name": "金融领域",
  "version": "1.0.0",
  "last_updated": "2026-04-06",
  "metadata": {
    "description": "金融领域专业术语词典",
    "language": "zh",
    "contributors": ["Meeting Notes Assistant Team"]
  },
  "terms": [
    {
      "term": "股权质押",
      "aliases": ["股权质押率", "质押率"],
      "category": "融资",
      "priority": "high",
      "correction_rules": [
        {"from": "古权质押", "to": "股权质押"},
        {"from": "古全质押", "to": "股权质押"}
      ]
    },
    {
      "term": "市盈率",
      "aliases": ["PE", "P/E Ratio", "估值倍数"],
      "category": "估值",
      "priority": "high",
      "correction_rules": []
    }
  ],
  "post_processing_rules": [
    {
      "pattern": "([0-9]+)倍市盈率",
      "replacement": "\\1x PE",
      "description": "标准化市盈率表达"
    }
  ]
}
```

### 2.3 词典管理器
```python
# scripts/domain_dictionary.py

from typing import Dict, List
import json
import re
from pathlib import Path

class DomainDictionary:
    """领域词典加载与匹配"""
    
    def __init__(self, dictionary_path: str = "domain-dictionaries"):
        self.dictionary_path = Path(dictionary_path)
        self.dictionaries = self._load_all_domains()
        self.active_domain = "general"  # 默认使用通用词典
    
    def _load_all_domains(self) -> Dict[str, Dict]:
        """加载所有领域词典"""
        dictionaries = {}
        
        for json_file in self.dictionary_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                domain_dict = json.load(f)
                domain = domain_dict['domain']
                dictionaries[domain] = domain_dict
        
        return dictionaries
    
    def set_domain(self, domain: str):
        """设置当前领域"""
        if domain in self.dictionaries:
            self.active_domain = domain
        else:
            print(f"⚠️  领域 '{domain}' 不存在，使用通用词典")
            self.active_domain = "general"
    
    def correct_terms(self, text: str) -> str:
        """根据当前领域的词典修正文本"""
        if not self.dictionaries:
            return text
        
        domain_dict = self.dictionaries[self.active_domain]
        
        # Step 1: 应用术语修正规则
        for term in domain_dict.get("terms", []):
            for rule in term.get("correction_rules", []):
                text = text.replace(rule["from"], rule["to"])
        
        # Step 2: 应用后处理规则（正则）
        for rule in domain_dict.get("post_processing_rules", []):
            pattern = rule["pattern"]
            replacement = rule["replacement"]
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def get_term_info(self, term: str) -> Dict:
        """获取术语信息"""
        domain_dict = self.dictionaries[self.active_domain]
        
        for term_info in domain_dict.get("terms", []):
            if term == term_info["term"] or term in term_info.get("aliases", []):
                return term_info
        
        return None
```

---

## Layer 3: 领域自适应层

### 3.1 领域检测器
```python
# scripts/domain_detector.py

from typing import Dict, Tuple, List

class DomainDetector:
    """自动检测会议所属领域"""
    
    def __init__(self, dictionary: DomainDictionary):
        self.dictionary = dictionary
    
    def detect_domain(self, text: str) -> Tuple[str, float]:
        """
        检测文本所属领域
        
        Returns:
            (领域名称, 置信度)
        """
        domain_scores = {}
        
        for domain_name, domain_dict in self.dictionary.dictionaries.items():
            score = 0
            term_count = 0
            
            for term in domain_dict.get("terms", []):
                # 检查术语出现次数
                count = text.count(term["term"])
                term_count += count
                
                # 检查别名出现次数
                for alias in term.get("aliases", []):
                    count += text.count(alias)
                    term_count += count
                
                # 权重 = 出现次数 × 优先级
                priority_weight = {"high": 3, "medium": 2, "low": 1}
                priority = term.get("priority", "medium")
                score += count * priority_weight.get(priority, 2)
            
            domain_scores[domain_name] = {
                "score": score,
                "term_count": term_count
            }
        
        # 归一化
        total_score = sum(d["score"] for d in domain_scores.values())
        
        if total_score == 0:
            return ("general", 0.0)
        
        normalized_scores = {
            domain: d["score"] / total_score 
            for domain, d in domain_scores.items()
        }
        
        # 找到最佳领域
        best_domain = max(normalized_scores.items(), key=lambda x: x[1])
        return best_domain
    
    def detect_mixed_domains(self, text: str, threshold: float = 0.2) -> List[str]:
        """
        检测混合领域
        
        Returns:
            置信度超过阈值的领域列表
        """
        domain, confidence = self.detect_domain(text)
        
        # 重新计算所有领域分数
        domain_scores = {}
        for domain_name, domain_dict in self.dictionary.dictionaries.items():
            score = 0
            for term in domain_dict.get("terms", []):
                score += text.count(term["term"])
            domain_scores[domain_name] = score
        
        total_score = sum(domain_scores.values())
        if total_score == 0:
            return ["general"]
        
        normalized_scores = {
            domain: score / total_score 
            for domain, score in domain_scores.items()
        }
        
        # 返回置信度 > threshold 的领域
        detected_domains = [
            domain for domain, conf in normalized_scores.items()
            if conf > threshold
        ]
        
        if not detected_domains:
            return ["general"]
        
        # 按置信度排序
        detected_domains.sort(
            key=lambda d: normalized_scores[d],
            reverse=True
        )
        
        return detected_domains
```

### 3.2 用户自定义词典支持
```python
# scripts/custom_dictionary.py

class CustomDictionary:
    """用户自定义词典"""
    
    def __init__(self, custom_path: str = ".workbuddy/custom-dictionaries"):
        self.custom_path = Path(custom_path)
        self.custom_dicts = self._load_custom_dicts()
    
    def _load_custom_dicts(self) -> Dict[str, Dict]:
        """加载用户自定义词典"""
        custom_dicts = {}
        
        if not self.custom_path.exists():
            return custom_dicts
        
        for json_file in self.custom_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                custom_dict = json.load(f)
                custom_dicts[custom_dict['domain']] = custom_dict
        
        return custom_dicts
    
    def add_term(self, domain: str, term: str, aliases: List[str] = None):
        """添加自定义术语"""
        if domain not in self.custom_dicts:
            self.custom_dicts[domain] = {
                "domain": domain,
                "name": f"{domain} (自定义)",
                "version": "1.0.0",
                "terms": []
            }
        
        term_entry = {
            "term": term,
            "aliases": aliases or [],
            "priority": "high",
            "correction_rules": []
        }
        
        self.custom_dicts[domain]["terms"].append(term_entry)
        self._save_custom_dict(domain)
    
    def _save_custom_dict(self, domain: str):
        """保存自定义词典"""
        self.custom_path.mkdir(parents=True, exist_ok=True)
        
        file_path = self.custom_path / f"{domain}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.custom_dicts[domain], f, ensure_ascii=False, indent=2)
```

---

## 完整工作流集成

```python
# scripts/transcribe_with_domain.py

from base_transcriber import BaseTranscriber
from domain_dictionary import DomainDictionary
from domain_detector import DomainDetector
from custom_dictionary import CustomDictionary

class DomainAwareTranscriber:
    """领域感知转写器"""
    
    def __init__(self, model_size: str = "large-v3"):
        # Layer 1: 基础转写
        self.transcriber = BaseTranscriber(model_size=model_size)
        
        # Layer 2: 领域词典
        self.dictionary = DomainDictionary()
        
        # Layer 3: 领域检测
        self.detector = DomainDetector(self.dictionary)
        
        # 自定义词典
        self.custom_dict = CustomDictionary()
    
    def transcribe(
        self, 
        audio_path: str, 
        domain: str = None,
        language: str = None
    ) -> Dict:
        """
        完整转写流程
        
        Args:
            audio_path: 音频文件路径
            domain: 指定领域（可选，None 表示自动检测）
            language: 语言代码（可选）
        
        Returns:
            {
                "text": "修正后的转写文本",
                "raw_text": "原始转写文本",
                "summary": "会议摘要",
                "domain": "检测到的领域",
                "confidence": 0.85,
                "terms": [...],
                "language": "zh"
            }
        """
        print("=" * 60)
        print("开始转写")
        print("=" * 60)
        
        # Step 1: 基础转写
        print("\n📝 Step 1: 基础转写 (Whisper large-v3)...")
        result = self.transcriber.transcribe(audio_path, language)
        raw_text = result["text"]
        print(f"✓ 基础转写完成: {len(raw_text)} 字符")
        
        # Step 2: 领域检测（如果未指定）
        if domain:
            print(f"\n🎯 指定领域: {domain}")
            detected_domain = domain
            confidence = 1.0
        else:
            print(f"\n🔍 Step 2: 自动检测领域...")
            detected_domain, confidence = self.detector.detect_domain(raw_text)
            print(f"✓ 检测到领域: {detected_domain} (置信度: {confidence:.2%})")
        
        # Step 3: 术语修正
        print(f"\n🔧 Step 3: 领域词典修正...")
        self.dictionary.set_domain(detected_domain)
        corrected_text = self.dictionary.correct_terms(raw_text)
        print(f"✓ 术语修正完成")
        
        # Step 4: 摘要与后处理
        print(f"\n📊 Step 4: 生成摘要...")
        summary = self._generate_summary(corrected_text, detected_domain)
        terms = self._extract_terms(corrected_text, detected_domain)
        print(f"✓ 摘要生成完成")
        
        print("\n" + "=" * 60)
        print("转写完成！")
        print("=" * 60)
        
        return {
            "text": corrected_text,
            "raw_text": raw_text,
            "summary": summary,
            "domain": detected_domain,
            "confidence": confidence,
            "terms": terms,
            "language": result.get("language", "zh")
        }
    
    def _generate_summary(self, text: str, domain: str) -> str:
        """生成会议摘要（简化版）"""
        # TODO: 集成更强大的摘要生成（如使用 LLM）
        lines = text.split("\n")
        return "\n".join(lines[:10]) + "\n..."
    
    def _extract_terms(self, text: str, domain: str) -> List[Dict]:
        """提取专业术语"""
        self.dictionary.set_domain(domain)
        domain_dict = self.dictionary.dictionaries[domain]
        
        found_terms = []
        for term_info in domain_dict.get("terms", []):
            term = term_info["term"]
            count = text.count(term)
            if count > 0:
                found_terms.append({
                    "term": term,
                    "count": count,
                    "category": term_info.get("category", "")
                })
        
        # 按出现次数排序
        found_terms.sort(key=lambda x: x["count"], reverse=True)
        return found_terms[:20]  # 返回前 20 个
```

---

## 使用示例

### 示例 1: 自动检测领域
```python
transcriber = DomainAwareTranscriber(model_size="large-v3")
result = transcriber.transcribe("meeting_audio.m4a")

print(f"检测到的领域: {result['domain']}")
print(f"置信度: {result['confidence']:.2%}")
print(f"修正后的文本: {result['text']}")
```

### 示例 2: 指定领域
```python
transcriber = DomainAwareTranscriber(model_size="large-v3")
result = transcriber.transcribe(
    "meeting_audio.m4a",
    domain="finance"  # 指定金融领域
)
```

### 示例 3: 添加自定义术语
```python
custom_dict = CustomDictionary()
custom_dict.add_term(
    domain="finance",
    term="方正证券",
    aliases=["方正", "方正证券公司"]
)
```

---

## 实施计划

### Phase 1: 基础设施（1-2 天）
- [x] 设计词典结构
- [x] 实现 `DomainDictionary` 类
- [x] 实现 `DomainDetector` 类
- [ ] 构建 `general.json` 和 `finance.json`
- [ ] 实现 `DomainAwareTranscriber` 类

### Phase 2: 核心领域（3-5 天）
- [ ] 构建 `technology.json`（500+ 术语）
- [ ] 构建 `healthcare.json`（500+ 术语）
- [ ] 构建 `legal.json`（500+ 术语）
- [ ] 测试混合领域识别
- [ ] 优化领域检测算法

### Phase 3: 优化与扩展（持续）
- [ ] 根据使用反馈优化词典
- [ ] 增加更多领域词典
- [ ] 优化领域检测算法
- [ ] 添加用户自定义词典功能
- [ ] 集成更强大的摘要生成（LLM）

---

## 性能优化

### 1. 词典加载优化
- 使用缓存机制，避免重复加载
- 支持增量更新词典

### 2. 术语匹配优化
- 使用 Aho-Corasick 算法优化多模式匹配
- 预编译正则表达式

### 3. 领域检测优化
- 限制扫描文本长度（前 5000 字符）
- 使用术语优先级加权
- 支持领域白名单/黑名单

---

## 总结

这个领域自适应架构让 `meeting-notes-assistant` 具备：

1. ✅ **通用性**: 基于 Whisper large-v3，支持所有语言和行业
2. ✅ **专业性**: 领域词典修正专业术语
3. ✅ **智能化**: 自动检测领域，无需人工干预
4. ✅ **可扩展**: 易于添加新领域词典
5. ✅ **用户友好**: 支持用户自定义术语

**这是一个真正的通用会议转写与摘要平台，不局限于任何特定领域。**
