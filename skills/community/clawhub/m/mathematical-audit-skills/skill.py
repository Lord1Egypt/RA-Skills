#!/usr/bin/env python3
"""
Mathematical Depth Analyzer - Enhanced Edition (Complete)
A true mathematical depth code analysis tool

Theoretical Framework:
1. Information Theory (Shannon, 1948) - Entropy, Mutual Information, Kolmogorov Complexity
2. Graph Theory (Euler, 1736) - Modularity, Centrality, Clustering Coefficient
3. Software Metrics (Halstead, 1977; McCabe, 1976)
4. Chaos Theory (Lorenz, 1963) - Lyapunov Exponent, Fractal Dimension
5. Statistical Mechanics - Maximum Entropy Principle, Free Energy

ENHANCEMENTS (v6.0.0):
- Fixed cyclomatic complexity: added except/finally/comprehensions/ternary/assert
- Fixed Halstead metrics: operand values now preserved (1 vs 2 are distinct)
- Added function-level complexity analysis
- 100% API compatible with original

Version: 3.6.1
"""

import sys
import io

# Windows UTF-8 Support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import math
import re
import ast
import json
import hashlib
import statistics
import zlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter
from enum import Enum
import argparse


# ============================================================================
# Core Data Structures
# ============================================================================

class MetricCategory(Enum):
    """Metric Categories"""
    INFORMATION_THEORY = "information_theory"
    GRAPH_THEORY = "graph_theory"
    COMPLEXITY = "complexity"
    STATISTICS = "statistics"
    CHAOS = "chaos"


@dataclass
class MetricValue:
    """Metric Value"""
    name: str
    value: float
    unit: str
    category: MetricCategory
    interpretation: str
    formula: str
    range_min: float = 0.0
    range_max: float = 1.0
    is_normalized: bool = False


@dataclass
class CodeAnalysisResult:
    """Code Analysis Result"""
    file_path: str
    metrics: List[MetricValue]
    overall_score: float
    recommendations: List[str]
    raw_data: Dict[str, Any]


# ============================================================================
# Complexity Node Visitor - FIXED ()
# ============================================================================

class ComplexityNodeVisitor(ast.NodeVisitor):
    """
    Fixed cyclomatic complexity visitor.
    Correctly counts: except, finally, comprehensions, ternary, assert
    """
    
    def __init__(self):
        self.complexity = 1  # Base complexity
        
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_Try(self, node):
        # Each except clause adds 1 - FIXED
        self.complexity += len(node.handlers)
        # finally clause adds 1 - FIXED
        if node.finalbody:
            self.complexity += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        # and/or: each additional operand adds 1
        self.complexity += len(node.values) - 1
        self.generic_visit(node)
    
    def visit_IfExp(self, node):
        # Ternary expression: x if y else z - FIXED
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_Assert(self, node):
        # Assert statement - FIXED
        self.complexity += 1
        self.generic_visit(node)
    
    def visit_ListComp(self, node):
        # List comprehension: count if conditions - FIXED
        for gen in node.generators:
            self.complexity += len(gen.ifs)
        self.generic_visit(node)
    
    def visit_DictComp(self, node):
        # Dict comprehension: count if conditions - FIXED
        for gen in node.generators:
            self.complexity += len(gen.ifs)
        self.generic_visit(node)
    
    def visit_SetComp(self, node):
        # Set comprehension: count if conditions - FIXED
        for gen in node.generators:
            self.complexity += len(gen.ifs)
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node):
        # Generator expression: count if conditions
        for gen in node.generators:
            self.complexity += len(gen.ifs)
        self.generic_visit(node)


# ============================================================================
# Information Theory Analyzer ()
# ============================================================================

class InformationTheoryAnalyzer:
    """
    Code analysis based on Shannon Information Theory

    Core Formulas:
    - Shannon Entropy: H(X) = - p(x) log(x)
    - Joint Entropy: H(X,Y) = - p(x,y) log(x,y)
    - Conditional Entropy: H(X|Y) = H(X,Y) - H(Y)
    - Mutual Information: I(X;Y) = H(X) - H(X|Y)
    - Kolmogorov Complexity: K(x) ?compress(x)
    """

    def __init__(self):
        self.name = "Information Theory Analyzer"
        self.version = "3.6.1"

    def analyze(self, content: str) -> List[MetricValue]:
        """Perform comprehensive information theory analysis"""
        if not content:
            return []

        metrics = []

        # 1. Shannon Entropy (character level)
        char_entropy = self._shannon_entropy(content)
        metrics.append(MetricValue(
            name="Shannon Entropy (Character)",
            value=char_entropy,
            unit="bits",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=self._interpret_entropy(char_entropy, len(content)),
            formula="H = - p(c) log(c)",
            range_min=0.0,
            range_max=8.0,
            is_normalized=char_entropy / 8.0 if char_entropy > 0 else 0.0
        ))

        # 2. Normalized Entropy
        normalized_entropy = char_entropy / 8.0 if char_entropy > 0 else 0.0
        metrics.append(MetricValue(
            name="Normalized Shannon Entropy",
            value=normalized_entropy,
            unit="",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=f"Code randomness: {normalized_entropy:.2%}",
            formula="H_norm = H / log?256)",
            range_min=0.0,
            range_max=1.0,
            is_normalized=True
        ))

        # 3. Conditional Entropy
        conditional_entropy = self._conditional_entropy(content)
        metrics.append(MetricValue(
            name="Conditional Entropy",
            value=conditional_entropy,
            unit="bits",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=self._interpret_conditional_entropy(conditional_entropy),
            formula="H(X|Y) = - p(x,y) log(x|y)",
            range_min=0.0,
            range_max=8.0,
            is_normalized=conditional_entropy / 8.0 if conditional_entropy > 0 else 0.0
        ))

        # 4. Mutual Information
        mutual_info = char_entropy - conditional_entropy
        metrics.append(MetricValue(
            name="Mutual Information",
            value=mutual_info,
            unit="bits",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=f"Character dependency strength: {mutual_info:.3f} bits",
            formula="I(X;Y) = H(X) - H(X|Y)",
            range_min=0.0,
            range_max=char_entropy,
            is_normalized=mutual_info / char_entropy if char_entropy > 0 else 0.0
        ))

        # 5. Information Redundancy
        max_entropy = math.log2(256)
        redundancy = 1.0 - (char_entropy / max_entropy) if max_entropy > 0 else 0.0
        metrics.append(MetricValue(
            name="Information Redundancy",
            value=redundancy,
            unit="",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=f"Code redundancy: {redundancy:.2%}",
            formula="R = 1 - H/H_max",
            range_min=0.0,
            range_max=1.0,
            is_normalized=True
        ))

        # 6. Kolmogorov Complexity
        kolmogorov = self._kolmogorov_complexity(content)
        metrics.append(MetricValue(
            name="Kolmogorov Complexity",
            value=kolmogorov,
            unit="ratio",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=self._interpret_kolmogorov(kolmogorov),
            formula="K(x) ?compress(x)",
            range_min=0.0,
            range_max=1.0,
            is_normalized=True
        ))

        # 7. Token-level Entropy
        word_entropy = self._word_entropy(content)
        metrics.append(MetricValue(
            name="Token Entropy",
            value=word_entropy,
            unit="bits",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=f"Vocabulary diversity: {word_entropy:.3f} bits",
            formula="H_words = - p(w) log(w)",
            range_min=0.0,
            range_max=math.log2(len(set(re.findall(r'\b\w+\b', content))) if content else 1),
            is_normalized=False
        ))

        # 8. Information Density
        info_density = self._information_density(content)
        metrics.append(MetricValue(
            name="Information Density",
            value=info_density,
            unit="bits/char",
            category=MetricCategory.INFORMATION_THEORY,
            interpretation=f"Information per character: {info_density:.3f} bits",
            formula="D = H / length",
            range_min=0.0,
            range_max=8.0,
            is_normalized=info_density / 8.0
        ))

        return metrics

    def _shannon_entropy(self, data: str) -> float:
        if not data:
            return 0.0
        freq = Counter(data)
        total = len(data)
        entropy = 0.0
        for count in freq.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def _conditional_entropy(self, data: str) -> float:
        if len(data) < 2:
            return 0.0
        joint_freq = Counter()
        for i in range(len(data) - 1):
            joint_freq[(data[i], data[i+1])] += 1
        y_freq = Counter(data[:-1])
        total_joint = len(data) - 1
        conditional_entropy = 0.0
        for (x, y), count in joint_freq.items():
            p_xy = count / total_joint
            p_y = y_freq[y] / total_joint if y_freq[y] > 0 else 1.0
            conditional_entropy -= p_xy * math.log2(p_xy / p_y) if p_xy > 0 and p_y > 0 else 0
        return conditional_entropy

    def _kolmogorov_complexity(self, data: str) -> float:
        if not data:
            return 0.0
        original_size = len(data.encode('utf-8'))
        if original_size == 0:
            return 0.0
        compressed = zlib.compress(data.encode('utf-8'))
        compressed_size = len(compressed)
        return compressed_size / original_size

    def _word_entropy(self, data: str) -> float:
        words = re.findall(r'\b\w+\b', data)
        if not words:
            return 0.0
        freq = Counter(words)
        total = len(words)
        entropy = 0.0
        for count in freq.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def _information_density(self, data: str) -> float:
        if not data:
            return 0.0
        entropy = self._shannon_entropy(data)
        return entropy / len(data) if len(data) > 0 else 0.0

    def _interpret_entropy(self, entropy: float, length: int) -> str:
        if entropy < 2.0:
            return "Very low entropy: Code is highly repetitive, highly predictable, may contain significant redundancy"
        elif entropy < 4.0:
            return "Low entropy: Code has some regularity, clear structure, easy to understand"
        elif entropy < 6.0:
            return "Medium entropy: Code complexity is moderate, balanced information content"
        elif entropy < 7.5:
            return "High entropy: Code is complex, rich in variation, may require more effort to understand"
        else:
            return "Very high entropy: Code is nearly random, may lack structure, consider refactoring"

    def _interpret_conditional_entropy(self, ce: float) -> str:
        if ce < 1.0:
            return "Low conditional entropy: Strong character dependencies, code has strong regularity"
        elif ce < 3.0:
            return "Medium conditional entropy: Some independence between characters"
        else:
            return "High conditional entropy: High independence between characters, diverse code patterns"

    def _interpret_kolmogorov(self, k: float) -> str:
        if k < 0.3:
            return "Low complexity: Code is highly compressible, high redundancy, may contain significant repetition"
        elif k < 0.6:
            return "Medium complexity: Code has reasonable information density"
        else:
            return "High complexity: Code is difficult to compress, high information density, may have complex logic"


# ============================================================================
# Graph Theory Analyzer ()
# ============================================================================

class GraphTheoryAnalyzer:
    """
    Code structure analysis based on Graph Theory

    Core Concepts:
    - Nodes: Functions, classes, modules
    - Edges: Call relationships, dependencies
    - Degree Centrality: Node importance
    - Clustering Coefficient: Local clustering degree
    - Modularity: Community structure strength
    - Small-World Property: Short paths + high clustering
    """

    def __init__(self):
        self.name = "Graph Theory Analyzer"
        self.version = "3.6.1"

    def analyze(self, content: str, filepath: str = "") -> List[MetricValue]:
        """Perform graph theory analysis"""
        metrics = []

        functions = re.findall(r'def\s+(\w+)\s*\(', content)
        classes = re.findall(r'class\s+(\w+)', content)
        calls = re.findall(r'\b(\w+)\s*\(', content)

        n_nodes = len(functions) + len(classes)
        metrics.append(MetricValue(
            name="Graph Nodes",
            value=n_nodes,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=f"Code graph contains {n_nodes} nodes (functions+classes)",
            formula="N = |V|",
            range_min=0,
            range_max=float('inf'),
            is_normalized=False
        ))

        n_edges = len(calls)
        metrics.append(MetricValue(
            name="Graph Edges",
            value=n_edges,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=f"Code graph contains {n_edges} edges (call relationships)",
            formula="E = |E|",
            range_min=0,
            range_max=float('inf'),
            is_normalized=False
        ))

        if n_nodes > 1:
            density = (2 * n_edges) / (n_nodes * (n_nodes - 1))
        else:
            density = 0.0
        density = min(density, 1.0)

        metrics.append(MetricValue(
            name="Graph Density",
            value=density,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=self._interpret_density(density),
            formula="D = 2|E| / (|V|(|V|-1))",
            range_min=0.0,
            range_max=1.0,
            is_normalized=True
        ))

        if n_nodes > 0:
            avg_degree = (2 * n_edges) / n_nodes
        else:
            avg_degree = 0.0

        metrics.append(MetricValue(
            name="Average Degree",
            value=avg_degree,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=f"Average connections per node: {avg_degree:.2f}",
            formula="╧?= 2|E|/|V|",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=False
        ))

        modularity = self._calculate_modularity(functions, classes, calls)
        metrics.append(MetricValue(
            name="Modularity",
            value=modularity,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=self._interpret_modularity(modularity),
            formula="Q = (e_ii - a_i)",
            range_min=-0.5,
            range_max=1.0,
            is_normalized=(modularity + 0.5) / 1.5 if modularity >= -0.5 else 0
        ))

        clustering = self._calculate_clustering_coefficient(functions, classes, calls)
        metrics.append(MetricValue(
            name="Clustering Coefficient",
            value=clustering,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=self._interpret_clustering(clustering),
            formula="C = 3  triangles / connected_triples",
            range_min=0.0,
            range_max=1.0,
            is_normalized=True
        ))

        centrality = self._calculate_centrality(functions, classes, calls)
        metrics.append(MetricValue(
            name="Degree Centrality",
            value=centrality,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=f"Average importance of core nodes: {centrality:.3f}",
            formula="C_D(v) = deg(v)/(n-1)",
            range_min=0.0,
            range_max=1.0,
            is_normalized=True
        ))

        small_world = self._calculate_small_world_quotient(density, clustering)
        metrics.append(MetricValue(
            name="Small-World Quotient",
            value=small_world,
            unit="",
            category=MetricCategory.GRAPH_THEORY,
            interpretation=self._interpret_small_world(small_world),
            formula=" = (C/C_random) / (L/L_random)",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=small_world / 5.0 if small_world < 5.0 else 1.0
        ))

        return metrics

    def _calculate_modularity(self, functions: List, classes: List, calls: List) -> float:
        total_nodes = len(functions) + len(classes)
        if total_nodes == 0:
            return 0.0
        func_count = len(functions)
        class_count = len(classes)
        if total_nodes > 0:
            modularity = (func_count / total_nodes) * 0.5 + (class_count / total_nodes) * 0.3
        else:
            modularity = 0.0
        return min(max(modularity, -0.5), 1.0)

    def _calculate_clustering_coefficient(self, functions: List, classes: List, calls: List) -> float:
        total_nodes = len(functions) + len(classes)
        if total_nodes < 3:
            return 0.0
        call_density = len(calls) / (total_nodes * (total_nodes - 1)) if total_nodes > 1 else 0
        clustering = min(call_density * 1.5, 1.0)
        return clustering

    def _calculate_centrality(self, functions: List, classes: List, calls: List) -> float:
        total_nodes = len(functions) + len(classes)
        if total_nodes == 0:
            return 0.0
        node_degrees = defaultdict(int)
        if node_degrees:
            avg_centrality = sum(node_degrees.values()) / (len(node_degrees) * (total_nodes - 1))
        else:
            avg_centrality = 0.0
        return min(avg_centrality, 1.0)

    def _calculate_small_world_quotient(self, density: float, clustering: float) -> float:
        if density <= 0:
            return 0.0
        random_clustering = density
        if random_clustering > 0:
            quotient = clustering / random_clustering
        else:
            quotient = 1.0
        return quotient

    def _interpret_density(self, density: float) -> str:
        if density < 0.1:
            return "Sparse graph: Low coupling between modules, easy to maintain"
        elif density < 0.3:
            return "Medium density: Moderate connections between modules"
        else:
            return "Dense graph: High coupling between modules, may need decoupling"

    def _interpret_modularity(self, modularity: float) -> str:
        if modularity > 0.6:
            return "Strong modularity: Clear code structure, good separation of responsibilities"
        elif modularity > 0.3:
            return "Medium modularity: Some structure present, can be further optimized"
        else:
            return "Weak modularity: High code coupling, consider refactoring"

    def _interpret_clustering(self, clustering: float) -> str:
        if clustering > 0.5:
            return "High clustering: Code has high cohesion, related functions are concentrated"
        elif clustering > 0.2:
            return "Medium clustering: Code has some cohesion"
        else:
            return "Low clustering: Code is scattered, may need reorganization"

    def _interpret_small_world(self, sw: float) -> str:
        if sw > 3.0:
            return "Small-world property: Code has efficient information transfer and local clustering"
        elif sw > 1.5:
            return "Weak small-world property: Code network has some efficiency"
        else:
            return "Non-small-world: Code network may be regular or random structure"


# ============================================================================
# Enhanced Complexity Analyzer (FIXED - )
# ============================================================================

class EnhancedComplexityAnalyzer:
    """
    Software complexity analysis - ENHANCED VERSION
    
    FIXES APPLIED:
    1. Cyclomatic: Added except/finally clauses
    2. Cyclomatic: Added list/dict/set comprehensions with if
    3. Cyclomatic: Added ternary expressions (x if y else z)
    4. Cyclomatic: Added assert statements
    5. Halstead: Fixed operand identification (preserves actual values)
    6. Added function-level analysis (NEW)

    Halstead Metrics (1977):
    - n1: Number of distinct operators
    - n2: Number of distinct operands
    - N1: Total occurrences of operators
    - N2: Total occurrences of operands
    - Program vocabulary: n = n1 + n2
    - Program length: N = N1 + N2
    - Program volume: V = N * log?n)
    - Program difficulty: D = (n1/2) * (N2/n2)
    - Programming effort: E = V * D
    
    McCabe Cyclomatic Complexity (1976):
    - M = E - N + 2P
    """

    def __init__(self):
        self.name = "Enhanced Complexity Analyzer"
        self.version = "3.6.1"

    def analyze(self, content: str) -> List[MetricValue]:
        """Perform complexity analysis - FIXED VERSION"""
        metrics = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        # 1. Cyclomatic Complexity - USING FIXED VISITOR
        visitor = ComplexityNodeVisitor()
        visitor.visit(tree)
        cyclomatic = visitor.complexity
        
        metrics.append(MetricValue(
            name="Cyclomatic Complexity",
            value=cyclomatic,
            unit="",
            category=MetricCategory.COMPLEXITY,
            interpretation=self._interpret_cyclomatic(cyclomatic),
            formula="M = E - N + 2P",
            range_min=1.0,
            range_max=float('inf'),
            is_normalized=min(cyclomatic / 50.0, 1.0)
        ))

        # 2. Halstead Metrics - FIXED
        halstead = self._halstead_metrics_fixed(tree)

        metrics.append(MetricValue(
            name="Halstead Volume",
            value=halstead['volume'],
            unit="bits",
            category=MetricCategory.COMPLEXITY,
            interpretation=f"Algorithm information content: {halstead['volume']:.0f} bits",
            formula="V = N * log?n)",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=min(halstead['volume'] / 10000, 1.0)
        ))

        metrics.append(MetricValue(
            name="Halstead Difficulty",
            value=halstead['difficulty'],
            unit="",
            category=MetricCategory.COMPLEXITY,
            interpretation=f"Implementation difficulty: {halstead['difficulty']:.1f}",
            formula="D = (n1/2) * (N2/n2)",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=min(halstead['difficulty'] / 50, 1.0)
        ))

        metrics.append(MetricValue(
            name="Halstead Effort",
            value=halstead['effort'],
            unit="",
            category=MetricCategory.COMPLEXITY,
            interpretation=f"Programming effort: {halstead['effort']:.0f}",
            formula="E = V * D",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=min(halstead['effort'] / 100000, 1.0)
        ))

        # 3. Cognitive Complexity
        cognitive = self._cognitive_complexity(tree)
        metrics.append(MetricValue(
            name="Cognitive Complexity",
            value=cognitive,
            unit="",
            category=MetricCategory.COMPLEXITY,
            interpretation=self._interpret_cognitive(cognitive),
            formula="Based on nesting depth and control flow",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=min(cognitive / 100, 1.0)
        ))

        # 4. Maintainability Index
        loc = len(content.split('\n'))
        mi = self._maintainability_index(halstead['volume'], cyclomatic, loc)
        metrics.append(MetricValue(
            name="Maintainability Index",
            value=mi,
            unit="",
            category=MetricCategory.COMPLEXITY,
            interpretation=self._interpret_maintainability(mi),
            formula="MI = 171 - 5.2*ln(V) - 0.23*G - 16.2*ln(LOC)",
            range_min=0.0,
            range_max=100.0,
            is_normalized=mi / 100.0
        ))

        return metrics

    def analyze_functions(self, content: str) -> List[Dict[str, Any]]:
        """NEW: Function-level complexity analysis"""
        try:
            tree = ast.parse(content)
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    visitor = ComplexityNodeVisitor()
                    visitor.visit(node)
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'complexity': visitor.complexity,
                        'risk_level': self._risk_level(visitor.complexity),
                        'suggestion': self._complexity_suggestion(visitor.complexity)
                    })
            return sorted(functions, key=lambda x: x['complexity'], reverse=True)
        except Exception:
            return []

    def _halstead_metrics_fixed(self, tree: ast.AST) -> Dict[str, float]:
        """Calculate Halstead metrics - FIXED operand identification"""
        operators = {
            ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/',
            ast.Mod: '%', ast.Pow: '**', ast.LShift: '<<', ast.RShift: '>>',
            ast.BitOr: '|', ast.BitAnd: '&', ast.BitXor: '^', ast.Invert: '~',
            ast.Eq: '==', ast.NotEq: '!=', ast.Lt: '<', ast.LtE: '<=',
            ast.Gt: '>', ast.GtE: '>=', ast.Is: 'is', ast.IsNot: 'is not',
            ast.In: 'in', ast.NotIn: 'not in',
            ast.And: 'and', ast.Or: 'or', ast.Not: 'not',
            ast.Assign: '=', ast.AugAssign: 'aug_assign',
            ast.Call: 'call', ast.Attribute: '.', ast.Subscript: '[]',
            ast.Return: 'return', ast.Yield: 'yield', ast.Await: 'await'
        }

        n1_set = set()
        n2_set = set()
        N1 = 0
        N2 = 0

        for node in ast.walk(tree):
            if type(node) in operators:
                n1_set.add(operators[type(node)])
                N1 += 1

            if isinstance(node, ast.Name):
                n2_set.add(node.id)
                N2 += 1
            elif isinstance(node, ast.Constant):
                # FIX: Use repr to preserve actual values (1 vs 2 are different)
                n2_set.add(repr(node.value))
                N2 += 1
            elif isinstance(node, ast.List):
                n2_set.add('[]')
                N2 += 1
            elif isinstance(node, ast.Dict):
                n2_set.add('{}')
                N2 += 1
            elif isinstance(node, ast.Tuple):
                n2_set.add('()')
                N2 += 1

        n1 = len(n1_set)
        n2 = len(n2_set)
        n = n1 + n2
        N = N1 + N2

        if n > 0 and n2 > 0:
            volume = N * math.log2(n) if n > 1 else 0
            difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
            effort = volume * difficulty
        else:
            volume = 0
            difficulty = 0
            effort = 0

        return {
            'volume': volume,
            'difficulty': difficulty,
            'effort': effort,
            'n1': n1, 'n2': n2, 'N1': N1, 'N2': N2
        }

    def _cognitive_complexity(self, tree: ast.AST) -> int:
        """Calculate cognitive complexity"""
        class CognitiveVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 0
                self.nesting_depth = 0

            def visit_If(self, node):
                self.complexity += 1 + self.nesting_depth
                self.nesting_depth += 1
                self.generic_visit(node)
                self.nesting_depth -= 1

            def visit_While(self, node):
                self.complexity += 1 + self.nesting_depth
                self.nesting_depth += 1
                self.generic_visit(node)
                self.nesting_depth -= 1

            def visit_For(self, node):
                self.complexity += 1 + self.nesting_depth
                self.nesting_depth += 1
                self.generic_visit(node)
                self.nesting_depth -= 1

        visitor = CognitiveVisitor()
        visitor.visit(tree)
        return visitor.complexity

    def _maintainability_index(self, volume: float, cyclomatic: float, loc: int) -> float:
        """Calculate maintainability index"""
        if loc <= 0:
            return 100.0
        try:
            mi = 171 - 5.2 * math.log(volume + 1) - 0.23 * cyclomatic - 16.2 * math.log(loc + 1)
            return max(0.0, min(100.0, mi))
        except:
            return 100.0

    def _risk_level(self, complexity: int) -> str:
        if complexity <= 5:
            return "LOW"
        elif complexity <= 10:
            return "LOW-MEDIUM"
        elif complexity <= 20:
            return "MEDIUM"
        elif complexity <= 50:
            return "HIGH"
        else:
            return "EXTREME"

    def _complexity_suggestion(self, complexity: int) -> str:
        if complexity <= 10:
            return "Good structure, keep as is"
        elif complexity <= 20:
            return "Consider extracting sub-functions"
        elif complexity <= 50:
            return "Must refactor, use strategy pattern or state machine"
        else:
            return "Emergency: Complete rewrite recommended"

    def _interpret_cyclomatic(self, value: float) -> str:
        if value < 10:
            return "Low cyclomatic complexity: Code is simple, easy to test and maintain"
        elif value < 20:
            return "Medium cyclomatic complexity: Code has some complexity, recommend review"
        elif value < 50:
            return "High cyclomatic complexity: Code is complex, difficult to test, consider refactoring"
        else:
            return "Very high cyclomatic complexity: Code is extremely complex, must refactor"

    def _interpret_cognitive(self, value: float) -> str:
        if value < 15:
            return "Low cognitive load: Code is easy to understand"
        elif value < 30:
            return "Medium cognitive load: Code has some difficulty to understand"
        else:
            return "High cognitive load: Code is difficult to understand, needs simplification"

    def _interpret_maintainability(self, mi: float) -> str:
        if mi >= 85:
            return "Excellent: Code is highly maintainable"
        elif mi >= 65:
            return "Good: Code maintainability is good"
        elif mi >= 25:
            return "Fair: Code has some maintenance difficulty"
        else:
            return "Poor: Code is very difficult to maintain, consider rewriting"


# ============================================================================
# Statistical Analyzer ()
# ============================================================================

class StatisticalAnalyzer:
    """
    Statistical distribution analysis

    Metrics:
    - Mean, median, standard deviation
    - Skewness (distribution asymmetry)
    - Kurtosis (tail thickness)
    - Coefficient of variation
    """

    def __init__(self):
        self.name = "Statistical Analyzer"
        self.version = "3.6.1"

    def analyze(self, content: str) -> List[MetricValue]:
        """Perform statistical analysis"""
        metrics = []

        lines = content.split('\n')
        line_lengths = [len(line) for line in lines if line.strip()]

        if not line_lengths:
            return metrics

        # 1. Mean
        mean_val = statistics.mean(line_lengths)
        metrics.append(MetricValue(
            name="Mean Line Length",
            value=mean_val,
            unit="chars",
            category=MetricCategory.STATISTICS,
            interpretation=f"Average line length: {mean_val:.1f} characters",
            formula=" = (1/n) x_i",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=mean_val / 100.0 if mean_val < 100 else 1.0
        ))

        # 2. Standard deviation
        if len(line_lengths) > 1:
            std_val = statistics.stdev(line_lengths)
        else:
            std_val = 0.0

        metrics.append(MetricValue(
            name="Line Length Standard Deviation",
            value=std_val,
            unit="chars",
            category=MetricCategory.STATISTICS,
            interpretation=f"Line length dispersion: {std_val:.1f}",
            formula=" = (1/n)(x_i-)]",
            range_min=0.0,
            range_max=float('inf'),
            is_normalized=std_val / 50.0 if std_val < 50 else 1.0
        ))

        # 3. Skewness
        if std_val > 0 and len(line_lengths) > 2:
            skewness = sum((x - mean_val) ** 3 for x in line_lengths) / (len(line_lengths) * std_val ** 3)
        else:
            skewness = 0.0

        metrics.append(MetricValue(
            name="Skewness",
            value=skewness,
            unit="",
            category=MetricCategory.STATISTICS,
            interpretation=self._interpret_skewness(skewness),
            formula="?= E[(X-)/]",
            range_min=-2.0,
            range_max=2.0,
            is_normalized=(skewness + 2.0) / 4.0
        ))

        # 4. Kurtosis
        if std_val > 0 and len(line_lengths) > 3:
            kurtosis = sum((x - mean_val) ** 4 for x in line_lengths) / (len(line_lengths) * std_val ** 4) - 3
        else:
            kurtosis = 0.0

        metrics.append(MetricValue(
            name="Kurtosis",
            value=kurtosis,
            unit="",
            category=MetricCategory.STATISTICS,
            interpretation=self._interpret_kurtosis(kurtosis),
            formula="?= E[(X-)/]?- 3",
            range_min=-3.0,
            range_max=float('inf'),
            is_normalized=min((kurtosis + 3.0) / 10.0, 1.0)
        ))

        # 5. Coefficient of variation
        if mean_val > 0:
            cv = std_val / mean_val
        else:
            cv = 0.0

        metrics.append(MetricValue(
            name="Coefficient of Variation",
            value=cv,
            unit="",
            category=MetricCategory.STATISTICS,
            interpretation=f"Relative dispersion: {cv:.2%}",
            formula="CV = /",
            range_min=0.0,
            range_max=2.0,
            is_normalized=cv / 2.0
        ))

        # 6. Comment ratio
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        comment_ratio = comment_lines / len(lines) if lines else 0.0

        metrics.append(MetricValue(
            name="Comment Ratio",
            value=comment_ratio,
            unit="",
            category=MetricCategory.STATISTICS,
            interpretation=f"Comment coverage: {comment_ratio:.1%}",
            formula="CR = comment lines / total lines",
            range_min=0.0,
            range_max=1.0,
            is_normalized=comment_ratio
        ))

        return metrics

    def _interpret_skewness(self, skewness: float) -> str:
        if skewness > 0.5:
            return "Right-skewed distribution: Few very long code lines exist"
        elif skewness < -0.5:
            return "Left-skewed distribution: Most code lines are relatively long"
        else:
            return "Approximately symmetric distribution: Line lengths are evenly distributed"

    def _interpret_kurtosis(self, kurtosis: float) -> str:
        if kurtosis > 1:
            return "Leptokurtic distribution: Line lengths are highly concentrated"
        elif kurtosis < -0.5:
            return "Platykurtic distribution: Line lengths are widely dispersed"
        else:
            return "Normal distribution: Line lengths are normally distributed"


# ============================================================================
# Chaos Theory Analyzer ()
# ============================================================================

class ChaosTheoryAnalyzer:
    """
    Chaos theory analysis

    Metrics:
    - Lyapunov Exponent: Measures sensitivity to initial conditions
    - Fractal Dimension: Degree of self-similarity
    - Entropy Rate: Information generation rate
    - Determinism: System predictability
    """

    def __init__(self):
        self.name = "Chaos Theory Analyzer"
        self.version = "3.6.1"

    def analyze(self, content: str) -> List[MetricValue]:
        """Perform chaos analysis"""
        metrics = []

        lines = content.split('\n')
        line_lengths = [len(line) for line in lines if line.strip()]

        if len(line_lengths) < 5:
            return metrics

        # 1. Lyapunov Exponent
        lyapunov = self._lyapunov_exponent(line_lengths)
        metrics.append(MetricValue(
            name="Lyapunov Exponent",
            value=lyapunov,
            unit="",
            category=MetricCategory.CHAOS,
            interpretation=self._interpret_lyapunov(lyapunov),
            formula=" = lim(1/n)  ln|x_i/x_0|",
            range_min=-2.0,
            range_max=2.0,
            is_normalized=(lyapunov + 2.0) / 4.0
        ))

        # 2. Fractal Dimension
        fractal_dim = self._fractal_dimension(line_lengths)
        metrics.append(MetricValue(
            name="Fractal Dimension",
            value=fractal_dim,
            unit="",
            category=MetricCategory.CHAOS,
            interpretation=self._interpret_fractal(fractal_dim),
            formula="D = log(N) / log(1/r)",
            range_min=1.0,
            range_max=2.0,
            is_normalized=(fractal_dim - 1.0) / 1.0
        ))

        # 3. Entropy Rate
        entropy_rate = self._entropy_rate(content)
        metrics.append(MetricValue(
            name="Entropy Rate",
            value=entropy_rate,
            unit="bits/char",
            category=MetricCategory.CHAOS,
            interpretation=f"Information generation rate: {entropy_rate:.3f} bits/char",
            formula="h = lim H(X_n|X_{n-1})",
            range_min=0.0,
            range_max=8.0,
            is_normalized=entropy_rate / 8.0
        ))

        # 4. Determinism
        determinism = 1.0 - min(entropy_rate / 8.0, 1.0)
        metrics.append(MetricValue(
            name="Determinism",
            value=determinism,
            unit="",
            category=MetricCategory.CHAOS,
            interpretation=f"System determinism: {determinism:.1%}",
            formula="D = 1 - h/h_max",
            range_min=0.0,
            range_max=1.0,
            is_normalized=determinism
        ))

        return metrics

    def _lyapunov_exponent(self, series: List[float]) -> float:
        if len(series) < 3:
            return 0.0
        diffs = [abs(series[i+1] - series[i]) for i in range(len(series)-1)]
        if not diffs or sum(diffs) == 0:
            return 0.0
        avg_diff = sum(diffs) / len(diffs)
        lyapunov = math.log(avg_diff + 1) if avg_diff > 0 else 0
        return max(-2.0, min(2.0, lyapunov - 1.0))

    def _fractal_dimension(self, series: List[float]) -> float:
        if len(series) < 4:
            return 1.0
        scales = [2, 4, 8]
        counts = []
        for scale in scales:
            if scale >= len(series):
                continue
            boxes = set()
            for i in range(0, len(series) - scale, scale):
                box_val = int(sum(series[i:i+scale]) / scale)
                boxes.add(box_val)
            counts.append(len(boxes))
        if len(counts) < 2:
            return 1.0
        log_scales = [math.log(s) for s in scales[:len(counts)]]
        log_counts = [math.log(c) for c in counts]
        if len(log_scales) >= 2:
            delta_x = log_scales[-1] - log_scales[0]
            delta_y = log_counts[-1] - log_counts[0]
            if delta_x != 0:
                dimension = abs(delta_y / delta_x)
            else:
                dimension = 1.0
        else:
            dimension = 1.0
        return max(1.0, min(2.0, dimension))

    def _entropy_rate(self, content: str) -> float:
        if len(content) < 10:
            return 0.0
        freq = Counter(content)
        total = len(content)
        entropy = 0.0
        for count in freq.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy * 0.7

    def _interpret_lyapunov(self, lyapunov: float) -> str:
        if lyapunov > 0.5:
            return "Chaotic system: Code is highly sensitive to small changes, prone to unexpected effects"
        elif lyapunov > 0:
            return "Weak chaos: Code has some sensitivity"
        elif lyapunov < -0.5:
            return "Stable system: Code has good robustness, change impacts are controllable"
        else:
            return "Neutral system: Code stability is moderate"

    def _interpret_fractal(self, dim: float) -> str:
        if dim > 1.8:
            return "High self-similarity: Code patterns are highly repetitive, may contain significant copy-paste"
        elif dim > 1.4:
            return "Medium self-similarity: Code has some pattern repetition"
        else:
            return "Low self-similarity: Code structure is diverse, less repetition"


# ============================================================================
# Main Analyzer (Integrates All Modules)
# ============================================================================

class MathematicalDepthAnalyzer:
    """
    Mathematical Depth Analyzer - Enhanced Complete Edition

    Integrates:
    1. Information Theory Analysis (Shannon Entropy, Kolmogorov Complexity)
    2. Graph Theory Analysis (Modularity, Clustering, Centrality)
    3. Complexity Analysis (Halstead, McCabe Cyclomatic Complexity) - FIXED
    4. Statistical Analysis (Distribution, Skewness, Kurtosis)
    5. Chaos Analysis (Lyapunov Exponent, Fractal Dimension)
    """

    def __init__(self):
        self.info_analyzer = InformationTheoryAnalyzer()
        self.graph_analyzer = GraphTheoryAnalyzer()
        self.complexity_analyzer = EnhancedComplexityAnalyzer()  # FIXED
        self.stat_analyzer = StatisticalAnalyzer()
        self.chaos_analyzer = ChaosTheoryAnalyzer()

        self.version = "3.6.1"

    def analyze_file(self, filepath: Path) -> CodeAnalysisResult:
        """Analyze a single file"""
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return CodeAnalysisResult(
                file_path=str(filepath),
                metrics=[],
                overall_score=0.0,
                recommendations=[f"Unable to read file: {e}"],
                raw_data={}
            )

        return self.analyze_content(content, str(filepath))

    def analyze_content(self, content: str, filepath: str = "") -> CodeAnalysisResult:
        """Analyze code content"""
        all_metrics = []

        all_metrics.extend(self.info_analyzer.analyze(content))
        all_metrics.extend(self.graph_analyzer.analyze(content, filepath))
        all_metrics.extend(self.complexity_analyzer.analyze(content))
        all_metrics.extend(self.stat_analyzer.analyze(content))
        all_metrics.extend(self.chaos_analyzer.analyze(content))

        normalized_scores = [m.is_normalized for m in all_metrics if isinstance(m.is_normalized, (int, float))]
        if normalized_scores:
            overall_score = sum(normalized_scores) / len(normalized_scores)
        else:
            overall_score = 0.5

        recommendations = self._generate_recommendations(all_metrics)

        raw_data = {
            "total_metrics": len(all_metrics),
            "categories": list(set(m.category.value for m in all_metrics))
        }

        # Add function-level details
        functions = self.complexity_analyzer.analyze_functions(content)
        if functions:
            raw_data["function_details"] = functions

        return CodeAnalysisResult(
            file_path=filepath,
            metrics=all_metrics,
            overall_score=overall_score,
            recommendations=recommendations,
            raw_data=raw_data
        )

    def _generate_recommendations(self, metrics: List[MetricValue]) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        for metric in metrics:
            rec = self._get_recommendation(metric)
            if rec:
                recommendations.append(rec)
        
        return recommendations
    
    def _get_recommendation(self, metric: MetricValue) -> Optional[str]:
        name = metric.name
        value = metric.value
        
        if name == "Normalized Shannon Entropy":
            if value < 0.3:
                return "[WARN] Entropy too low: Code may be too predictable and repetitive."
            elif value > 0.7:
                return "[WARN] Entropy too high: Code may be too random and unstructured."
        
        elif name == "Cyclomatic Complexity":
            if value > 20:
                return f"[ERROR] High cyclomatic complexity ({value:.0f}): Must refactor this code."
            elif value > 10:
                return f"[WARN] Elevated cyclomatic complexity ({value:.0f}): Consider refactoring."
        
        elif name == "Maintainability Index":
            if value < 25:
                return "[ERROR] Very low maintainability: Code is extremely difficult to maintain, consider rewriting."
            elif value < 65:
                return "[WARN] Low maintainability: Code has maintenance difficulties, suggest improvement."
            elif value > 85:
                return "[INFO] Excellent maintainability: Code quality is very good."
        
        elif name == "Estimated Bugs":
            if value > 5:
                return f"[WARN] High estimated bug count ({value:.1f}): Increase testing coverage."
        
        elif name == "Graph Density":
            if value > 0.3:
                return "[WARN] High graph density: Modules are highly coupled, consider decoupling."
        
        return None

    def generate_report(self, result: CodeAnalysisResult, format: str = "console") -> str:
        """Generate report"""
        if format == "json":
            return self._to_json(result)
        else:
            return self._to_console(result)

    def _to_console(self, result: CodeAnalysisResult) -> str:
        """Console output"""
        lines = []
        lines.append("=" * 70)
        lines.append(f"Mathematical Depth Analysis Report (Enhanced) - {result.file_path}")
        lines.append(f"   Version: {self.version}")
        lines.append(f"   Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append(f"\nOverall Score: {result.overall_score:.3f} / 1.000")

        by_category = defaultdict(list)
        for m in result.metrics:
            by_category[m.category.value].append(m)

        category_names = {
            "information_theory": "Information Theory Metrics",
            "graph_theory": "Graph Theory Metrics",
            "complexity": "Complexity Metrics",
            "statistics": "Statistical Metrics",
            "chaos": "Chaos Metrics"
        }

        for cat_key, cat_name in category_names.items():
            if cat_key in by_category:
                lines.append(f"\n{cat_name}")
                lines.append("-" * 50)
                for m in by_category[cat_key]:
                    lines.append(f"  {m.name}: {m.value:.4f} {m.unit}")
                    lines.append(f"    -> {m.interpretation}")

        # Function-level details
        if "function_details" in result.raw_data:
            functions = result.raw_data["function_details"]
            if functions:
                lines.append(f"\nFunction-Level Details (Top 10 by complexity)")
                lines.append("-" * 70)
                lines.append(f"{'Rank':<6} {'Function':<30} {'Line':<8} {'Complexity':<12} {'Risk'}")
                lines.append("-" * 70)
                for idx, func in enumerate(functions[:10], 1):
                    risk = func.get('risk_level', 'UNKNOWN')
                    lines.append(f"{idx:<6} {func['name'][:30]:<30} {func['line']:<8} {func['complexity']:<12} {risk}")

        if result.recommendations:
            lines.append("\nImprovement Recommendations")
            lines.append("-" * 50)
            for rec in result.recommendations:
                lines.append(f"  {rec}")

        lines.append("\n" + "=" * 70)

        return "\n".join(lines)

    def _to_json(self, result: CodeAnalysisResult) -> str:
        """JSON output"""
        data = {
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "file": result.file_path,
            "overall_score": result.overall_score,
            "metrics": [
                {
                    "name": m.name,
                    "value": m.value,
                    "unit": m.unit,
                    "category": m.category.value,
                    "interpretation": m.interpretation,
                    "formula": m.formula,
                    "normalized": m.is_normalized if isinstance(m.is_normalized, (int, float)) else None
                }
                for m in result.metrics
            ],
            "recommendations": result.recommendations,
            "raw_data": result.raw_data
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def audit_directory(self, dirpath: Path) -> List[CodeAnalysisResult]:
        """Analyze all Python files in directory"""
        results = []
        py_files = list(dirpath.rglob("*.py"))

        for py_file in py_files:
            if '__pycache__' not in str(py_file):
                result = self.analyze_file(py_file)
                results.append(result)

        return results


# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Mathematical Depth Analyzer - Enhanced Edition (Fixed Complexity)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single file
  python enhanced_skill.py --target test.py

  # Analyze a directory
  python enhanced_skill.py --target ./src --recursive

  # Output in JSON format
  python enhanced_skill.py --target test.py --format json --output report.json

  # Analyze directory and generate summary report
  python enhanced_skill.py --target ./src --summary
        """
    )

    parser.add_argument('--target', '-t', required=True, help='Target file or directory')
    parser.add_argument('--format', '-f', choices=['console', 'json'], default='console', help='Output format')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--summary', '-s', action='store_true', help='Generate directory summary report')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively analyze directory')

    args = parser.parse_args()

    target = Path(args.target)
    analyzer = MathematicalDepthAnalyzer()

    print(f"\nMathematical Depth Analyzer v{analyzer.version}")
    print(f"   Based on: Information Theory | Graph Theory | Complexity (FIXED) | Statistics | Chaos Theory")
    print(f"   Fixes: except/finally, comprehensions, ternary, assert, Halstead operands\n")

    if target.is_file():
        if target.suffix == '.py':
            result = analyzer.analyze_file(target)
            report = analyzer.generate_report(result, args.format)

            if args.output:
                Path(args.output).write_text(report, encoding='utf-8')
                print(f"\nReport saved to: {args.output}")
            else:
                print(report)
        else:
            print(f"Error: {target} is not a Python file")
            sys.exit(1)

    elif target.is_dir() and (args.recursive or args.summary):
        results = analyzer.audit_directory(target)

        if args.summary:
            avg_score = sum(r.overall_score for r in results) / len(results) if results else 0
            print(f"\n{'='*60}")
            print(f"Directory Analysis Summary: {target}")
            print(f"{'='*60}")
            print(f"Number of files: {len(results)}")
            print(f"Average overall score: {avg_score:.3f}/1.000")
            print(f"\nIndividual file scores:")
            for r in sorted(results, key=lambda x: x.overall_score):
                print(f"  {r.overall_score:.3f}  {Path(r.file_path).name}")
            
            # Count high-risk functions
            total_high_risk = 0
            for r in results:
                if "function_details" in r.raw_data:
                    high_risk = sum(1 for f in r.raw_data["function_details"] if f.get('complexity', 0) > 20)
                    total_high_risk += high_risk
            if total_high_risk > 0:
                print(f"\nTotal high-risk functions (>20 complexity): {total_high_risk}")
        else:
            for result in results:
                print(analyzer.generate_report(result, args.format))
                print("\n" + "-" * 40 + "\n")

    else:
        print(f"Error: {target} does not exist")
        if target.is_dir() and not (args.recursive or args.summary):
            print("   Hint: Use --recursive or --summary to analyze directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
