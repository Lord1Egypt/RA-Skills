#!/usr/bin/env python3
"""
Math Problem Processor
Converts images containing math problems to structured formulas and solutions
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import base64

@dataclass
class FormulaExtract:
    """Extracted mathematical formula with metadata"""
    original_text: str
    latex: str
    description: str
    problem_context: str
    confidence: float

@dataclass
class MathProblem:
    """Structured math problem from image"""
    problem_id: str
    raw_text: str
    problem_statement: str
    formulas: List[FormulaExtract]
    domain: str  # algebra, geometry, calculus, etc.
    difficulty: str  # elementary, intermediate, advanced
    extracted_at: str

class MathFormulaConverter:
    """Convert various mathematical notations to LaTeX"""
    
    # Common mathematical patterns
    PATTERNS = {
        # Fractions
        r'(\d+)/(\d+)': lambda m: f'\\frac{{{m.group(1)}}}{{{m.group(2)}}}',
        r'(\w)/(\w)': lambda m: f'\\frac{{{m.group(1)}}}{{{m.group(2)}}}',
        
        # Exponents
        r'(\w)\^(\d+)': lambda m: f'{m.group(1)}^{{{m.group(2)}}}',
        r'(\w)\^(\w)': lambda m: f'{m.group(1)}^{{{m.group(2)}}}',
        
        # Square roots
        r'sqrt\(([^)]+)\)': lambda m: f'\\sqrt{{{m.group(1)}}}',
        r'√([^\s]+)': lambda m: f'\\sqrt{{{m.group(1)}}}',
        
        # Greek letters
        r'\bpi\b': '\\pi',
        r'\balpha\b': '\\alpha',
        r'\bbeta\b': '\\beta',
        r'\bgamma\b': '\\gamma',
        r'\bdelta\b': '\\delta',
        r'\bsigma\b': '\\sigma',
        r'\blambda\b': '\\lambda',
        r'\btheta\b': '\\theta',
        
        # Summation
        r'sum\((\w+)=(\d+)\s+to\s+(\w+)\)': lambda m: f'\\sum_{{{m.group(1)}={m.group(2)}}}^{{{m.group(3)}}}',
        r'∑': '\\sum',
        
        # Integral
        r'integral\s+(.+)\s+d(\w)': lambda m: f'\\int {m.group(1)} d{m.group(2)}',
        r'∫': '\\int',
        
        # Limit
        r'lim\s+(\w+)→(\w+)': lambda m: f'\\lim_{{{m.group(1)}\\to {m.group(2)}}}',
        
        # Infinity
        r'infinity|∞': '\\infty',
        
        # Absolute value
        r'\|([^|]+)\|': lambda m: f'\\left|{m.group(1)}\\right|',
        
        # Equals with conditions
        r'(\w+)\s*=\s*(.+)\s+when\s+(.+)': lambda m: f'{m.group(1)} = {m.group(2)} \\text{{ when }} {m.group(3)}',
    }
    
    @classmethod
    def to_latex(cls, text: str) -> str:
        """Convert mathematical notation to LaTeX"""
        result = text
        
        # Apply pattern conversions
        for pattern, replacement in cls.PATTERNS.items():
            if callable(replacement):
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
            else:
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Clean up whitespace
        result = re.sub(r'\s+', ' ', result).strip()
        
        return result
    
    @classmethod
    def validate_latex(cls, latex: str) -> Tuple[bool, Optional[str]]:
        """Validate LaTeX formula syntax"""
        # Check balanced braces
        if latex.count('{') != latex.count('}'):
            return False, "Unbalanced braces in LaTeX"
        
        # Check common LaTeX commands are properly formatted
        invalid_patterns = [
            r'\\\s+\w',  # Commands with space before argument
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, latex):
                return False, f"Invalid LaTeX pattern: {pattern}"
        
        return True, None

class MathProblemAnalyzer:
    """Analyze extracted text to identify mathematical domains and difficulty"""
    
    DOMAIN_KEYWORDS = {
        'algebra': ['equation', 'solve', 'factor', 'expand', 'simplify', 'polynomial', 'linear', 'quadratic'],
        'geometry': ['angle', 'triangle', 'circle', 'area', 'perimeter', 'volume', 'radius', 'diameter'],
        'calculus': ['derivative', 'integral', 'limit', 'continuous', 'differentiable', 'function'],
        'statistics': ['mean', 'variance', 'probability', 'distribution', 'correlation', 'hypothesis'],
        'linear_algebra': ['matrix', 'vector', 'determinant', 'eigenvalue', 'linear transformation'],
        'trigonometry': ['sin', 'cos', 'tan', 'angle', 'radian', 'degree', 'periodic'],
    }
    
    DIFFICULTY_INDICATORS = {
        'elementary': ['simple', 'basic', 'first', 'grade', 'primary'],
        'intermediate': ['solve', 'find', 'calculate', 'prove'],
        'advanced': ['prove', 'generalize', 'theorem', 'complex', 'abstract'],
    }
    
    @classmethod
    def identify_domain(cls, text: str) -> str:
        """Identify mathematical domain from problem text"""
        text_lower = text.lower()
        scores = {}
        
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[domain] = score
        
        return max(scores, key=scores.get) if scores else 'general'
    
    @classmethod
    def assess_difficulty(cls, text: str) -> str:
        """Assess problem difficulty"""
        text_lower = text.lower()
        scores = {'elementary': 0, 'intermediate': 1, 'advanced': 2}
        
        for difficulty, keywords in cls.DIFFICULTY_INDICATORS.items():
            if any(kw in text_lower for kw in keywords):
                return difficulty
        
        return 'intermediate'

class MathProblemProcessor:
    """Main processor for math problem images"""
    
    def __init__(self):
        self.converter = MathFormulaConverter()
        self.analyzer = MathProblemAnalyzer()
    
    def extract_formulas(self, text: str) -> List[FormulaExtract]:
        """Extract mathematical formulas from text"""
        formulas = []
        
        # Simple extraction - split by common delimiters
        # This would be enhanced by actual OCR output structure
        formula_patterns = [
            r'[a-zA-Z0-9+\-*/()^√∫∑=]+',
        ]
        
        for i, match in enumerate(re.finditer(r'[a-zA-Z0-9+\-*/()^√∫∑=]+', text)):
            formula_text = match.group()
            if len(formula_text) > 2:  # Filter very short matches
                latex = self.converter.to_latex(formula_text)
                valid, error = self.converter.validate_latex(latex)
                
                if valid:
                    formulas.append(FormulaExtract(
                        original_text=formula_text,
                        latex=latex,
                        description=f"Formula {i+1}",
                        problem_context=text,
                        confidence=0.85
                    ))
        
        return formulas
    
    def process(self, problem_text: str, problem_id: str = None) -> MathProblem:
        """Process a math problem from text"""
        
        if not problem_id:
            problem_id = f"prob_{hash(problem_text) % 10000}"
        
        # Extract formulas
        formulas = self.extract_formulas(problem_text)
        
        # Analyze problem
        domain = self.analyzer.identify_domain(problem_text)
        difficulty = self.analyzer.assess_difficulty(problem_text)
        
        return MathProblem(
            problem_id=problem_id,
            raw_text=problem_text,
            problem_statement=problem_text[:200] + "..." if len(problem_text) > 200 else problem_text,
            formulas=formulas,
            domain=domain,
            difficulty=difficulty,
            extracted_at=__import__('datetime').datetime.now().isoformat()
        )
    
    def to_dict(self, problem: MathProblem) -> Dict:
        """Convert MathProblem to dictionary"""
        data = asdict(problem)
        data['formulas'] = [asdict(f) for f in problem.formulas]
        return data
    
    def to_json(self, problem: MathProblem) -> str:
        """Convert MathProblem to JSON"""
        return json.dumps(self.to_dict(problem), ensure_ascii=False, indent=2)

def main():
    """CLI interface for math problem processing"""
    if len(sys.argv) < 2:
        print("Usage: process_math_problem.py '<problem_text>' [problem_id]")
        print("\nExample:")
        print('  process_math_problem.py "Solve: x^2 + 2x + 1 = 0" prob_001')
        sys.exit(1)
    
    problem_text = sys.argv[1]
    problem_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    processor = MathProblemProcessor()
    problem = processor.process(problem_text, problem_id)
    
    print(processor.to_json(problem))

if __name__ == '__main__':
    main()
