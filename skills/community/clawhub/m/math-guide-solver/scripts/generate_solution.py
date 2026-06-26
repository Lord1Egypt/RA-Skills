#!/usr/bin/env python3
"""
Math Solution Generator
Generates guided solutions with Socratic method and detailed explanations
"""

import json
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

class SolutionMode(Enum):
    """Solution generation modes"""
    SOCRATIC = "socratic"  # Ask guiding questions
    DETAILED = "detailed"   # Full step-by-step
    QUICK = "quick"        # Just the answer

class Theme(Enum):
    """PNG rendering themes"""
    LIGHT = "light"
    DARK = "dark"
    SEPIA = "sepia"
    CHALK = "chalk"

@dataclass
class SolutionStep:
    """Single step in solution"""
    step_number: int
    description: str
    latex_formula: Optional[str] = None
    hint: Optional[str] = None
    explanation: Optional[str] = None

class SocraticGuide:
    """Generate Socratic method guidance"""
    
    SOCRATIC_PATTERNS = {
        'understanding': [
            "What is the problem asking you to find?",
            "Can you restate the problem in your own words?",
            "What information do you have?",
            "What are you solving for?",
        ],
        'concept_identification': [
            "What mathematical concept does this relate to?",
            "Which formula or theorem applies here?",
            "Have you seen a similar problem before?",
            "What's the relationship between the given information?",
        ],
        'method': [
            "What approach would you use?",
            "What's your first step?",
            "What method could you apply?",
            "Can you think of multiple ways to solve this?",
        ],
        'execution': [
            "Can you show me your work?",
            "What's your next step?",
            "Does that follow from the previous step?",
            "Why did you do that?",
        ],
        'verification': [
            "Does your answer make sense?",
            "Can you check your answer another way?",
            "Is your answer in the correct form?",
            "Did you answer the question that was asked?",
        ],
    }
    
    @classmethod
    def generate_hints(cls, problem_domain: str, problem_type: str) -> List[str]:
        """Generate contextual hints based on problem type"""
        
        hints_db = {
            'quadratic_equation': [
                cls.SOCRATIC_PATTERNS['understanding'][1],
                "Can you identify a, b, and c?",
                "Which method would you try: factoring, quadratic formula, or completing the square?",
                "What do the solutions represent?",
            ],
            'fraction_addition': [
                cls.SOCRATIC_PATTERNS['understanding'][0],
                "What do we need to add fractions?",
                "What's the least common denominator?",
                "Can you rewrite each fraction with the common denominator?",
            ],
            'limit': [
                "What value does x approach?",
                "Can you directly substitute the value?",
                "What technique might work: factoring, rationalization, or L'Hôpital's rule?",
            ],
            'derivative': [
                "What's the function?",
                "Which differentiation rule applies?",
                "Can you apply the power rule, product rule, or chain rule?",
            ],
        }
        
        return hints_db.get(problem_type, cls.SOCRATIC_PATTERNS['understanding'])

class DetailedExplainer:
    """Generate detailed step-by-step explanations"""
    
    EXPLANATION_TEMPLATE = {
        'problem_restatement': "Problem: {problem}",
        'key_concept': "Key concept: {concept}",
        'formula': "Formula to use: {latex}",
        'step': "Step {num}: {description}",
        'verification': "Verification: {check}",
    }
    
    @classmethod
    def generate_solution(cls, problem: str, domain: str, solution_steps: List[SolutionStep]) -> str:
        """Generate detailed solution text"""
        
        output = []
        output.append(f"## Detailed Solution\n")
        output.append(f"**Problem:** {problem}\n")
        output.append(f"**Domain:** {domain.title()}\n\n")
        
        # Generate step-by-step
        for step in solution_steps:
            output.append(f"### Step {step.step_number}: {step.description}\n")
            
            if step.latex_formula:
                output.append(f"**Formula:** `{step.latex_formula}`\n")
            
            if step.explanation:
                output.append(f"**Explanation:** {step.explanation}\n")
            
            output.append("")
        
        return "\n".join(output)

@dataclass
class RenderConfig:
    """Configuration for formula rendering"""
    theme: Theme = Theme.LIGHT
    formula_size: str = "medium"  # small, medium, large
    dpi: int = 300
    background_transparent: bool = False
    include_explanation: bool = True
    inline_mode: bool = False  # Inline in text vs. separate image

class LaTeXRenderer:
    """Configure LaTeX rendering to PNG"""
    
    THEME_CONFIGS = {
        Theme.LIGHT: {
            'background': '#ffffff',
            'text_color': '#000000',
            'accent': '#0066cc',
        },
        Theme.DARK: {
            'background': '#1e1e1e',
            'text_color': '#ffffff',
            'accent': '#00d4ff',
        },
        Theme.SEPIA: {
            'background': '#f4f1de',
            'text_color': '#2d2d2d',
            'accent': '#d4a574',
        },
        Theme.CHALK: {
            'background': '#2c2c2c',
            'text_color': '#e0e0e0',
            'accent': '#ffeb3b',
        },
    }
    
    SIZE_CONFIGS = {
        'small': {'font_size': 10, 'padding': 5},
        'medium': {'font_size': 14, 'padding': 10},
        'large': {'font_size': 18, 'padding': 15},
    }
    
    @classmethod
    def get_render_command(cls, latex: str, config: RenderConfig) -> str:
        """Generate command to render LaTeX formula"""
        
        theme_cfg = cls.THEME_CONFIGS[config.theme]
        size_cfg = cls.SIZE_CONFIGS[config.formula_size]
        
        # This would be passed to math-images skill
        command = {
            'latex': latex,
            'theme': config.theme.value,
            'background_color': theme_cfg['background'],
            'text_color': theme_cfg['text_color'],
            'accent_color': theme_cfg['accent'],
            'font_size': size_cfg['font_size'],
            'padding': size_cfg['padding'],
            'dpi': config.dpi,
            'transparent': config.background_transparent,
            'include_explanation': config.include_explanation,
        }
        
        return json.dumps(command, indent=2)

class SolutionGenerator:
    """Main class to generate solutions"""
    
    def __init__(self, mode: SolutionMode = SolutionMode.SOCRATIC):
        self.mode = mode
        self.socratic = SocraticGuide()
        self.explainer = DetailedExplainer()
    
    def generate(self, 
                 problem: str, 
                 domain: str,
                 latex_formulas: List[str],
                 render_config: Optional[RenderConfig] = None) -> Dict:
        """Generate complete solution"""
        
        if render_config is None:
            render_config = RenderConfig()
        
        result = {
            'problem': problem,
            'domain': domain,
            'mode': self.mode.value,
            'formulas': latex_formulas,
        }
        
        if self.mode == SolutionMode.SOCRATIC:
            result['guidance'] = self._generate_socratic_guidance(problem, domain)
        elif self.mode == SolutionMode.DETAILED:
            result['solution'] = self._generate_detailed_solution(problem, domain, latex_formulas)
        elif self.mode == SolutionMode.QUICK:
            result['answer'] = "Solution pending - ask for detailed explanation"
        
        # Add rendering config for all formulas
        result['render_config'] = {
            'theme': render_config.theme.value,
            'formula_size': render_config.formula_size,
            'dpi': render_config.dpi,
        }
        
        return result
    
    def _generate_socratic_guidance(self, problem: str, domain: str) -> List[str]:
        """Generate Socratic questioning sequence"""
        hints = self.socratic.generate_hints(domain, 'general')
        return hints
    
    def _generate_detailed_solution(self, problem: str, domain: str, formulas: List[str]) -> str:
        """Generate detailed step-by-step solution"""
        steps = [
            SolutionStep(1, "Understand the problem", 
                        explanation="Identify what we need to find"),
            SolutionStep(2, "Extract formulas",
                        latex_formula=formulas[0] if formulas else None,
                        explanation="Identify relevant mathematical relationships"),
            SolutionStep(3, "Apply method",
                        explanation="Use appropriate mathematical technique"),
            SolutionStep(4, "Verify answer",
                        explanation="Check that answer is reasonable and correct"),
        ]
        
        return self.explainer.generate_solution(problem, domain, steps)

def main():
    """CLI interface"""
    if len(sys.argv) < 3:
        print("Usage: generate_solution.py '<problem>' <domain> [mode] [theme]")
        print("\nModes: socratic, detailed, quick")
        print("Themes: light, dark, sepia, chalk")
        sys.exit(1)
    
    problem = sys.argv[1]
    domain = sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'socratic'
    theme = sys.argv[4] if len(sys.argv) > 4 else 'light'
    
    solution_mode = SolutionMode[mode.upper()]
    render_theme = Theme[theme.upper()]
    
    generator = SolutionGenerator(solution_mode)
    render_config = RenderConfig(theme=render_theme)
    
    solution = generator.generate(problem, domain, [], render_config)
    print(json.dumps(solution, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
