"""
MR / PR Complexity Service - Provider-Agnostic Pull Request Complexity Measurement

Implements a 4-dimension complexity scoring framework:
1. SIZE (20%): Volume of code changed (logarithmic scale)
2. COGNITIVE (30%): Mental load - directory breadth, cross-module, file diversity
3. REVIEW EFFORT (30%): Discussion depth, reviewer count, review iterations
4. RISK/IMPACT (20%): Breaking changes, migrations, dependencies, security

Each dimension produces a 0-100 score, weighted to final complexity score.

Usage:
    calculator = MRComplexityCalculator()
    complexity = calculator.calculate(mr_data)
    # complexity.total_score, complexity.size_score, etc.
"""

import re
import math
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any
from pathlib import PurePosixPath

logger = logging.getLogger(__name__)


# =============================================================================
# CONFIGURATION - Tunable weights and thresholds
# =============================================================================

@dataclass
class ComplexityConfig:
    """Configurable weights and thresholds for complexity calculation"""
    
    # Dimension weights (must sum to 1.0)
    weight_size: float = 0.20
    weight_cognitive: float = 0.30
    weight_review: float = 0.30
    weight_risk: float = 0.20
    
    # Size dimension thresholds
    size_loc_log_multiplier: float = 20.0  # log10(loc+1) * this
    size_files_multiplier: float = 5.0     # files * this
    size_max_score: float = 100.0
    
    # Cognitive dimension thresholds
    cognitive_max_dirs: int = 8            # Cap at 8 unique directories
    cognitive_max_file_types: int = 5      # Cap at 5 file extensions
    cognitive_max_scatter: float = 3.0     # Max hunks/file ratio
    
    # Review dimension thresholds
    review_max_iterations: int = 4         # Cap review cycles
    review_max_reviewers: int = 5          # Cap reviewer count
    review_max_comment_density: float = 2.0  # Comments per file cap
    review_max_hours: float = 72.0         # Max hours to approval
    
    # Risk detection patterns
    risk_breaking_patterns: List[str] = field(default_factory=lambda: [
        r"BREAKING\s*CHANGE",
        r"BREAKING:",
        r"\[BREAKING\]",
        r"breaking-change",
    ])
    risk_migration_patterns: List[str] = field(default_factory=lambda: [
        r"/migrations?/",
        r"/db/",
        r"/schema/",
        r"\.sql$",
        r"alembic",
        r"flyway",
    ])
    risk_dependency_files: List[str] = field(default_factory=lambda: [
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "requirements.txt",
        "Pipfile",
        "Pipfile.lock",
        "pyproject.toml",
        "poetry.lock",
        "go.mod",
        "go.sum",
        "Cargo.toml",
        "Cargo.lock",
        "Gemfile",
        "Gemfile.lock",
        "pom.xml",
        "build.gradle",
    ])
    risk_security_patterns: List[str] = field(default_factory=lambda: [
        r"/auth/",
        r"/security/",
        r"/crypto/",
        r"/oauth/",
        r"/jwt/",
        r"password",
        r"secret",
        r"credential",
    ])
    
    # Cross-module detection (paths that indicate different domains)
    cross_module_markers: List[str] = field(default_factory=lambda: [
        "frontend",
        "backend",
        "api",
        "web",
        "mobile",
        "infra",
        "infrastructure",
        "terraform",
        "k8s",
        "kubernetes",
        "docker",
        "services",
        "lib",
        "shared",
        "common",
    ])


# Default configuration
DEFAULT_CONFIG = ComplexityConfig()


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ComplexityBreakdown:
    """Detailed breakdown of complexity scores by dimension"""
    
    # Final score
    total_score: float = 0.0
    
    # Dimension scores (0-100 each)
    size_score: float = 0.0
    cognitive_score: float = 0.0
    review_score: float = 0.0
    risk_score: float = 0.0
    
    # Size dimension details
    lines_changed: int = 0
    files_changed: int = 0
    net_lines: int = 0  # additions - deletions
    
    # Cognitive dimension details
    unique_directories: int = 0
    unique_file_types: int = 0
    is_cross_module: bool = False
    scatter_factor: float = 0.0  # hunks / files (if available)
    hotspot_ratio: float = 0.0   # % of files that are hotspots
    directories_touched: List[str] = field(default_factory=list)
    file_types_touched: List[str] = field(default_factory=list)
    modules_touched: List[str] = field(default_factory=list)
    
    # Review dimension details
    review_iterations: int = 0
    reviewers_count: int = 0
    discussions_count: int = 0
    comment_density: float = 0.0
    hours_to_approval: float = 0.0
    
    # Risk dimension details
    has_breaking_change: bool = False
    has_migration: bool = False
    has_dependency_change: bool = False
    has_security_change: bool = False
    linked_issues_count: int = 0
    risk_files: List[str] = field(default_factory=list)
    
    # Metadata
    complexity_tier: str = "moderate"  # trivial, simple, moderate, complex, highly_complex
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "total_score": round(self.total_score, 1),
            "dimensions": {
                "size": {
                    "score": round(self.size_score, 1),
                    "weight": DEFAULT_CONFIG.weight_size,
                    "lines_changed": self.lines_changed,
                    "files_changed": self.files_changed,
                    "net_lines": self.net_lines,
                    "insight": self._get_size_insight(),
                },
                "cognitive": {
                    "score": round(self.cognitive_score, 1),
                    "weight": DEFAULT_CONFIG.weight_cognitive,
                    "unique_directories": self.unique_directories,
                    "unique_file_types": self.unique_file_types,
                    "is_cross_module": self.is_cross_module,
                    "modules_touched": self.modules_touched,
                    "directories": self.directories_touched[:5],  # Top 5
                    "file_types": self.file_types_touched,
                    "insight": self._get_cognitive_insight(),
                },
                "review": {
                    "score": round(self.review_score, 1),
                    "weight": DEFAULT_CONFIG.weight_review,
                    "reviewers_count": self.reviewers_count,
                    "discussions_count": self.discussions_count,
                    "comment_density": round(self.comment_density, 2),
                    "review_iterations": self.review_iterations,
                    "hours_to_approval": round(self.hours_to_approval, 1) if self.hours_to_approval else None,
                    "insight": self._get_review_insight(),
                },
                "risk": {
                    "score": round(self.risk_score, 1),
                    "weight": DEFAULT_CONFIG.weight_risk,
                    "has_breaking_change": self.has_breaking_change,
                    "has_migration": self.has_migration,
                    "has_dependency_change": self.has_dependency_change,
                    "has_security_change": self.has_security_change,
                    "linked_issues_count": self.linked_issues_count,
                    "risk_files": self.risk_files[:5],  # Top 5
                    "insight": self._get_risk_insight(),
                },
            },
            "tier": self.complexity_tier,
            "tier_insight": self._get_tier_insight(),
        }
    
    def _get_size_insight(self) -> str:
        """Generate human-readable insight for size dimension"""
        if self.size_score < 20:
            return f"Small change ({self.lines_changed} LOC, {self.files_changed} files)"
        elif self.size_score < 40:
            return f"Moderate size ({self.lines_changed} LOC across {self.files_changed} files)"
        elif self.size_score < 60:
            return f"Substantial change ({self.lines_changed} LOC, {self.files_changed} files touched)"
        elif self.size_score < 80:
            return f"Large PR ({self.lines_changed} LOC impacting {self.files_changed} files)"
        else:
            return f"Very large PR ({self.lines_changed} LOC, {self.files_changed} files) - consider splitting"
    
    def _get_cognitive_insight(self) -> str:
        """Generate human-readable insight for cognitive dimension"""
        parts = []
        if self.is_cross_module:
            modules = ", ".join(self.modules_touched[:3])
            parts.append(f"crosses {len(self.modules_touched)} modules ({modules})")
        if self.unique_directories > 3:
            parts.append(f"spans {self.unique_directories} directories")
        if self.unique_file_types > 2:
            types = ", ".join(self.file_types_touched[:3])
            parts.append(f"touches {self.unique_file_types} file types ({types})")
        
        if not parts:
            if self.cognitive_score < 20:
                return "Single-focus change, easy to understand"
            return "Focused change within one area"
        
        base = "High mental load: " if self.cognitive_score >= 50 else "Moderate complexity: "
        return base + "; ".join(parts)
    
    def _get_review_insight(self) -> str:
        """Generate human-readable insight for review dimension"""
        parts = []
        if self.reviewers_count > 2:
            parts.append(f"{self.reviewers_count} reviewers involved")
        if self.discussions_count > 3:
            parts.append(f"{self.discussions_count} discussion threads")
        if self.review_iterations > 1:
            parts.append(f"{self.review_iterations} review rounds")
        if self.hours_to_approval and self.hours_to_approval > 24:
            days = round(self.hours_to_approval / 24, 1)
            parts.append(f"{days}d to approval")
        
        if not parts:
            if self.review_score < 20:
                return "Quick review, minimal discussion needed"
            return "Standard review process"
        
        return "Thorough review: " + "; ".join(parts)
    
    def _get_risk_insight(self) -> str:
        """Generate human-readable insight for risk dimension"""
        risks = []
        if self.has_breaking_change:
            risks.append("breaking API change")
        if self.has_migration:
            risks.append("database migration")
        if self.has_dependency_change:
            risks.append("dependency update")
        if self.has_security_change:
            risks.append("security-related code")
        if self.linked_issues_count > 2:
            risks.append(f"linked to {self.linked_issues_count} issues")
        
        if not risks:
            return "Low risk - no high-impact patterns detected"
        
        return "Risk factors: " + ", ".join(risks)
    
    def _get_tier_insight(self) -> str:
        """Generate insight explaining the complexity tier"""
        tier_descriptions = {
            "trivial": "Simple change requiring minimal review (typo, config, small fix)",
            "simple": "Straightforward change in one area, quick to review",
            "moderate": "Multi-file change requiring careful review",
            "complex": "Architectural or cross-module change needing deep review",
            "highly_complex": "Large-scale change with significant risk - extra scrutiny needed",
        }
        return tier_descriptions.get(self.complexity_tier, "Unknown tier")


@dataclass
class MRData:
    """Input data for complexity calculation"""
    # Basic info
    iid: int = 0
    title: str = ""
    description: str = ""
    
    # Size metrics
    additions: int = 0
    deletions: int = 0
    files_changed: int = 0
    
    # File paths (for cognitive and risk analysis)
    file_paths: List[str] = field(default_factory=list)
    
    # Labels
    labels: List[str] = field(default_factory=list)
    
    # Commit messages
    commit_messages: List[str] = field(default_factory=list)
    
    # Review metrics
    reviewers_count: int = 0
    discussions_count: int = 0
    review_iterations: int = 0  # Number of approval cycles
    hours_to_approval: Optional[float] = None
    
    # Linked issues (parsed from description)
    linked_issues: List[str] = field(default_factory=list)


# =============================================================================
# COMPLEXITY CALCULATOR
# =============================================================================

class MRComplexityCalculator:
    """
    Calculate MR complexity using the 4-dimension framework.
    
    Dimensions:
    1. SIZE (20%): Volume of code
    2. COGNITIVE (30%): Mental load to understand
    3. REVIEW EFFORT (30%): Effort required to review
    4. RISK/IMPACT (20%): Potential for problems if wrong
    """
    
    def __init__(self, config: ComplexityConfig = None):
        self.config = config or DEFAULT_CONFIG
        
        # Compile regex patterns for performance
        self._breaking_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.config.risk_breaking_patterns
        ]
        self._migration_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.config.risk_migration_patterns
        ]
        self._security_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.config.risk_security_patterns
        ]
    
    def calculate(self, mr: MRData) -> ComplexityBreakdown:
        """
        Calculate comprehensive complexity breakdown for an MR.
        
        Args:
            mr: MRData with all available information
            
        Returns:
            ComplexityBreakdown with scores and details
        """
        breakdown = ComplexityBreakdown()
        
        # Calculate each dimension
        self._calculate_size(mr, breakdown)
        self._calculate_cognitive(mr, breakdown)
        self._calculate_review(mr, breakdown)
        self._calculate_risk(mr, breakdown)
        
        # Calculate weighted total
        breakdown.total_score = (
            breakdown.size_score * self.config.weight_size +
            breakdown.cognitive_score * self.config.weight_cognitive +
            breakdown.review_score * self.config.weight_review +
            breakdown.risk_score * self.config.weight_risk
        )
        
        # Determine complexity tier
        breakdown.complexity_tier = self._get_tier(breakdown.total_score)
        
        return breakdown
    
    def _calculate_size(self, mr: MRData, breakdown: ComplexityBreakdown) -> None:
        """
        Calculate SIZE dimension score (0-100).
        
        Formula:
            size_score = min(100, log10(loc+1) * 20 + files * 5)
        
        Uses logarithmic scale to prevent gaming with huge PRs.
        """
        loc = mr.additions + mr.deletions
        breakdown.lines_changed = loc
        breakdown.files_changed = mr.files_changed
        breakdown.net_lines = mr.additions - mr.deletions
        
        # Logarithmic scaling for lines
        loc_component = math.log10(loc + 1) * self.config.size_loc_log_multiplier
        
        # Linear component for files
        files_component = mr.files_changed * self.config.size_files_multiplier
        
        breakdown.size_score = min(
            self.config.size_max_score,
            loc_component + files_component
        )
    
    def _calculate_cognitive(self, mr: MRData, breakdown: ComplexityBreakdown) -> None:
        """
        Calculate COGNITIVE dimension score (0-100).
        
        Components:
        - Unique directories touched (25%)
        - Cross-module flag (25%)
        - File type diversity (20%)
        - Scatter factor (15%) - if hunks available
        - Hotspot ratio (15%) - if available
        """
        if not mr.file_paths:
            # Fallback: estimate from files_changed
            breakdown.cognitive_score = min(100, mr.files_changed * 10)
            return
        
        # Extract directories
        directories = set()
        file_types = set()
        modules = set()
        
        for path in mr.file_paths:
            pp = PurePosixPath(path)
            
            # Get parent directory
            if pp.parent and str(pp.parent) != ".":
                directories.add(str(pp.parent))
            
            # Get file extension
            if pp.suffix:
                file_types.add(pp.suffix.lower())
            
            # Check for cross-module markers
            path_lower = path.lower()
            for marker in self.config.cross_module_markers:
                if f"/{marker}/" in path_lower or path_lower.startswith(f"{marker}/"):
                    modules.add(marker)
        
        breakdown.unique_directories = len(directories)
        breakdown.unique_file_types = len(file_types)
        breakdown.is_cross_module = len(modules) >= 2
        breakdown.directories_touched = sorted(directories)[:10]
        breakdown.file_types_touched = sorted(file_types)
        breakdown.modules_touched = sorted(modules)
        
        # Calculate component scores
        dir_score = (min(breakdown.unique_directories, self.config.cognitive_max_dirs) 
                    / self.config.cognitive_max_dirs) * 25
        
        cross_module_score = 25 if breakdown.is_cross_module else 0
        
        file_type_score = (min(breakdown.unique_file_types, self.config.cognitive_max_file_types)
                          / self.config.cognitive_max_file_types) * 20
        
        # Scatter factor (if we have hunk data, otherwise skip)
        scatter_score = 0  # Would need hunk data
        
        # Hotspot ratio (would need file history, otherwise skip)
        hotspot_score = 0  # Would need git history
        
        # For now, redistribute the missing 30% proportionally
        base_score = dir_score + cross_module_score + file_type_score
        breakdown.cognitive_score = min(100, base_score * (100 / 70))  # Scale up since we're missing 30%
    
    def _calculate_review(self, mr: MRData, breakdown: ComplexityBreakdown) -> None:
        """
        Calculate REVIEW EFFORT dimension score (0-100).
        
        Components:
        - Review iterations (30%)
        - Number of reviewers (20%)
        - Comment density (20%)
        - Time to approval (15%)
        - Substantive comments (15%) - approximated
        """
        breakdown.reviewers_count = mr.reviewers_count
        breakdown.discussions_count = mr.discussions_count
        breakdown.review_iterations = mr.review_iterations
        breakdown.hours_to_approval = mr.hours_to_approval or 0
        
        # Comment density = discussions / files
        breakdown.comment_density = (
            mr.discussions_count / max(mr.files_changed, 1)
        )
        
        # Calculate component scores
        iteration_score = (
            min(mr.review_iterations, self.config.review_max_iterations)
            / self.config.review_max_iterations
        ) * 30
        
        reviewer_score = (
            min(mr.reviewers_count, self.config.review_max_reviewers)
            / self.config.review_max_reviewers
        ) * 20
        
        density_score = (
            min(breakdown.comment_density, self.config.review_max_comment_density)
            / self.config.review_max_comment_density
        ) * 20
        
        time_score = 0
        if breakdown.hours_to_approval > 0:
            time_score = (
                min(breakdown.hours_to_approval, self.config.review_max_hours)
                / self.config.review_max_hours
            ) * 15
        
        # Substantive comments approximation (assume 70% are substantive)
        substantive_score = 0.7 * 15
        
        breakdown.review_score = min(
            100,
            iteration_score + reviewer_score + density_score + time_score + substantive_score
        )
    
    def _calculate_risk(self, mr: MRData, breakdown: ComplexityBreakdown) -> None:
        """
        Calculate RISK/IMPACT dimension score (0-100).
        
        Components:
        - Breaking change signal (25%)
        - Database/schema changes (25%)
        - Dependency updates (20%)
        - Linked issues count (15%)
        - Security/auth changes (15%)
        """
        risk_files = []
        
        # Check for breaking changes
        breakdown.has_breaking_change = self._check_breaking_change(mr)
        
        # Check for migrations
        for path in mr.file_paths:
            for pattern in self._migration_patterns:
                if pattern.search(path):
                    breakdown.has_migration = True
                    risk_files.append(path)
                    break
        
        # Check for dependency changes
        for path in mr.file_paths:
            filename = PurePosixPath(path).name
            if filename in self.config.risk_dependency_files:
                breakdown.has_dependency_change = True
                risk_files.append(path)
        
        # Check for security changes
        for path in mr.file_paths:
            for pattern in self._security_patterns:
                if pattern.search(path):
                    breakdown.has_security_change = True
                    risk_files.append(path)
                    break
        
        # Check labels for security
        for label in mr.labels:
            if "security" in label.lower():
                breakdown.has_security_change = True
        
        # Parse linked issues from description
        breakdown.linked_issues_count = len(mr.linked_issues) or self._count_linked_issues(mr.description)
        
        breakdown.risk_files = list(set(risk_files))
        
        # Calculate score
        breaking_score = 25 if breakdown.has_breaking_change else 0
        migration_score = 25 if breakdown.has_migration else 0
        dependency_score = 20 if breakdown.has_dependency_change else 0
        
        issues_score = (
            min(breakdown.linked_issues_count, 5) / 5
        ) * 15
        
        security_score = 15 if breakdown.has_security_change else 0
        
        breakdown.risk_score = min(
            100,
            breaking_score + migration_score + dependency_score + issues_score + security_score
        )
    
    def _check_breaking_change(self, mr: MRData) -> bool:
        """Check if MR indicates a breaking change"""
        # Check title
        for pattern in self._breaking_patterns:
            if pattern.search(mr.title):
                return True
        
        # Check labels
        for label in mr.labels:
            if "breaking" in label.lower():
                return True
        
        # Check commit messages
        for msg in mr.commit_messages:
            for pattern in self._breaking_patterns:
                if pattern.search(msg):
                    return True
        
        return False
    
    def _count_linked_issues(self, description: str) -> int:
        """Count linked issues in MR description"""
        if not description:
            return 0
        
        # Match patterns like #123, PROJ-123, closes #123, fixes PROJ-123
        patterns = [
            r"#(\d+)",  # GitHub style
            r"([A-Z]{2,10}-\d+)",  # JIRA style
            r"closes?\s+#?(\d+)",
            r"fixes?\s+#?(\d+)",
            r"resolves?\s+#?(\d+)",
        ]
        
        issues = set()
        for pattern in patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            issues.update(matches)
        
        return len(issues)
    
    def _get_tier(self, score: float) -> str:
        """Determine complexity tier from total score"""
        if score < 20:
            return "trivial"
        elif score < 40:
            return "simple"
        elif score < 60:
            return "moderate"
        elif score < 80:
            return "complex"
        else:
            return "highly_complex"
    
    def calculate_from_raw(
        self,
        additions: int = 0,
        deletions: int = 0,
        files_changed: int = 0,
        file_paths: List[str] = None,
        reviewers_count: int = 0,
        discussions_count: int = 0,
        labels: List[str] = None,
        title: str = "",
        description: str = "",
        commit_messages: List[str] = None,
        review_iterations: int = 1,
        hours_to_approval: float = None,
    ) -> ComplexityBreakdown:
        """
        Convenience method to calculate complexity from raw parameters.
        
        Use this when you don't want to construct an MRData object.
        """
        mr = MRData(
            title=title,
            description=description,
            additions=additions,
            deletions=deletions,
            files_changed=files_changed,
            file_paths=file_paths or [],
            labels=labels or [],
            commit_messages=commit_messages or [],
            reviewers_count=reviewers_count,
            discussions_count=discussions_count,
            review_iterations=review_iterations,
            hours_to_approval=hours_to_approval,
        )
        return self.calculate(mr)


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_calculator_instance: Optional[MRComplexityCalculator] = None


def get_mr_complexity_calculator() -> MRComplexityCalculator:
    """Get singleton instance of MRComplexityCalculator"""
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = MRComplexityCalculator()
    return _calculator_instance


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def calculate_mr_complexity(
    additions: int,
    deletions: int,
    files_changed: int,
    file_paths: List[str] = None,
    reviewers_count: int = 0,
    discussions_count: int = 0,
    **kwargs
) -> ComplexityBreakdown:
    """
    Quick utility function to calculate MR complexity.
    
    Example:
        complexity = calculate_mr_complexity(
            additions=150,
            deletions=30,
            files_changed=5,
            file_paths=["backend/auth/login.py", "frontend/src/Login.tsx"],
            reviewers_count=2,
            discussions_count=8,
        )
        print(f"Complexity: {complexity.total_score:.1f} ({complexity.complexity_tier})")
    """
    calculator = get_mr_complexity_calculator()
    return calculator.calculate_from_raw(
        additions=additions,
        deletions=deletions,
        files_changed=files_changed,
        file_paths=file_paths,
        reviewers_count=reviewers_count,
        discussions_count=discussions_count,
        **kwargs
    )


# =============================================================================
# CLI FOR TESTING
# =============================================================================

if __name__ == "__main__":
    # Example usage
    calculator = MRComplexityCalculator()
    
    # Test case 1: Simple typo fix
    simple = calculator.calculate_from_raw(
        additions=5,
        deletions=3,
        files_changed=1,
        file_paths=["README.md"],
        reviewers_count=1,
        discussions_count=0,
        title="Fix typo in README",
    )
    print(f"\n1. Simple typo fix:")
    print(f"   Total: {simple.total_score:.1f} ({simple.complexity_tier})")
    print(f"   Size: {simple.size_score:.1f}, Cognitive: {simple.cognitive_score:.1f}, "
          f"Review: {simple.review_score:.1f}, Risk: {simple.risk_score:.1f}")
    
    # Test case 2: Cross-module feature
    cross_module = calculator.calculate_from_raw(
        additions=350,
        deletions=50,
        files_changed=12,
        file_paths=[
            "backend/services/auth.py",
            "backend/routers/auth.py",
            "backend/models/user.py",
            "frontend/src/components/Login.tsx",
            "frontend/src/api/auth.ts",
            "frontend/src/hooks/useAuth.ts",
            "tests/backend/test_auth.py",
            "tests/frontend/Login.test.tsx",
            "docs/auth.md",
            "migrations/001_add_oauth.sql",
            "package.json",
            "requirements.txt",
        ],
        reviewers_count=3,
        discussions_count=15,
        labels=["feature", "breaking-change"],
        title="BREAKING: Add OAuth2 authentication",
        review_iterations=3,
        hours_to_approval=48,
    )
    print(f"\n2. Cross-module OAuth feature:")
    print(f"   Total: {cross_module.total_score:.1f} ({cross_module.complexity_tier})")
    print(f"   Size: {cross_module.size_score:.1f}, Cognitive: {cross_module.cognitive_score:.1f}, "
          f"Review: {cross_module.review_score:.1f}, Risk: {cross_module.risk_score:.1f}")
    print(f"   Breaking: {cross_module.has_breaking_change}, Migration: {cross_module.has_migration}, "
          f"Deps: {cross_module.has_dependency_change}")
    print(f"   Modules: {cross_module.modules_touched}")
    
    # Test case 3: Medium refactor
    refactor = calculator.calculate_from_raw(
        additions=200,
        deletions=180,
        files_changed=8,
        file_paths=[
            "backend/services/user_service.py",
            "backend/services/user_helper.py",
            "backend/utils/validators.py",
            "tests/test_user_service.py",
        ],
        reviewers_count=2,
        discussions_count=6,
        title="Refactor user service for better testability",
        description="Closes #123, fixes #456",
        review_iterations=2,
    )
    print(f"\n3. Medium refactor:")
    print(f"   Total: {refactor.total_score:.1f} ({refactor.complexity_tier})")
    print(f"   Size: {refactor.size_score:.1f}, Cognitive: {refactor.cognitive_score:.1f}, "
          f"Review: {refactor.review_score:.1f}, Risk: {refactor.risk_score:.1f}")
    print(f"   Linked issues: {refactor.linked_issues_count}")
