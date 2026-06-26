import pytest
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/prompt-optimizer-toolkit')

from scripts.prompt_optimizer import PromptOptimizer, PromptLibrary

class TestPromptOptimizer:
    def setup_method(self):
        self.optimizer = PromptOptimizer()
    
    def test_analyze_returns_dict(self):
        result = self.optimizer.analyze("Hello world")
        assert isinstance(result, dict)
    
    def test_analyze_has_required_keys(self):
        result = self.optimizer.analyze("Hello world")
        required = ["length", "word_count", "has_context", "has_constraints", 
                    "has_examples", "has_role", "has_structure", 
                    "clarity_score", "specificity_score", "overall_score"]
        for key in required:
            assert key in result
    
    def test_clarity_score_range(self):
        result = self.optimizer.analyze("Hello world")
        assert 0 <= result["clarity_score"] <= 10
    
    def test_specificity_score_range(self):
        result = self.optimizer.analyze("Hello world")
        assert 0 <= result["specificity_score"] <= 10
    
    def test_overall_score_range(self):
        result = self.optimizer.analyze("Hello world")
        assert 0 <= result["overall_score"] <= 10
    
    def test_empty_prompt(self):
        result = self.optimizer.analyze("")
        assert result["length"] == 0
    
    def test_optimize_returns_string(self):
        result = self.optimizer.optimize("Test prompt")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_optimize_auto_strategy(self):
        result = self.optimizer.optimize("Test prompt", strategy="auto")
        assert isinstance(result, str)
    
    def test_optimize_clarity_strategy(self):
        result = self.optimizer.optimize("Test prompt", strategy="clarity")
        assert isinstance(result, str)
    
    def test_apply_template_valid(self):
        result = self.optimizer.apply_template("chain_of_thought", task="calculate 2+2")
        assert isinstance(result, str)
        assert "step by step" in result.lower()
    
    def test_apply_template_invalid_raises(self):
        with pytest.raises(ValueError):
            self.optimizer.apply_template("nonexistent_template")
    
    def test_suggest_improvements_returns_list(self):
        result = self.optimizer.suggest_improvements("Write a story")
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_suggest_improvements_empty_prompt(self):
        result = self.optimizer.suggest_improvements("")
        assert isinstance(result, list)


class TestPromptLibrary:
    def setup_method(self):
        self.lib = PromptLibrary("test_prompts.json")
    
    def teardown_method(self):
        import os
        if os.path.exists("test_prompts.json"):
            os.remove("test_prompts.json")
    
    def test_save_and_get(self):
        self.lib.save("test-prompt", "Test content", tags=["test"])
        assert self.lib.get("test-prompt") == "Test content"
    
    def test_get_nonexistent(self):
        assert self.lib.get("nonexistent") is None
    
    def test_search_by_tag(self):
        self.lib.save("p1", "Content 1", tags=["coding"])
        self.lib.save("p2", "Content 2", tags=["coding"])
        self.lib.save("p3", "Content 3", tags=["writing"])
        
        coding = self.lib.search("coding")
        assert len(coding) == 2
        
        writing = self.lib.search("writing")
        assert len(writing) == 1
    
    def test_list_all(self):
        self.lib.save("p1", "Content 1")
        self.lib.save("p2", "Content 2")
        assert len(self.lib.list_all()) == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
