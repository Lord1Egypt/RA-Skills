"""
知识卡质量检查脚本 - 王琦教授中医体质学术助手

检查知识卡的完整性和质量，输出问题报告。

Usage:
    python validate_cards.py
    python validate_cards.py --fix  # 尝试自动修复简单问题
    python validate_cards.py --report report.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from card_cleaner import clean_authors, clean_card, clean_title, is_generic_knowledge_point, title_is_placeholder
from runtime_paths import DEFAULT_CARDS_DIR

# Required fields by source type
REQUIRED_FIELDS = {
    "paper": ["card_id", "source_type", "source_file", "year", "language"],
    "clinical_experience": ["card_id", "source_type", "source_file", "year", "language"]
}

# Recommended fields for better quality
RECOMMENDED_FIELDS = {
    "paper": ["title", "authors", "abstract", "conclusions", "keywords", "doi"],
    "clinical_experience": ["title", "authors", "clinical_insights", "diagnostic_approach"]
}

# Fields for citation/traceability
CITATION_FIELDS = ["citations", "evidence_sentences", "cross_references"]

# Fields for personality simulation
PERSONALITY_FIELDS = ["clinical_insights", "academic_innovation"]


@dataclass
class CardIssue:
    """Represents an issue found in a knowledge card"""
    card_id: str
    field: str
    issue_type: str  # missing, empty, low_quality, format_error
    severity: str  # critical, warning, info
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Validation result for a single card"""
    card_id: str
    source_type: str
    source_file: str
    issues: List[CardIssue] = field(default_factory=list)
    bonus_points: float = 0.0  # Bonus points for good quality fields
    
    @property
    def is_valid(self) -> bool:
        return not any(i.severity == "critical" for i in self.issues)
    
    @property
    def quality_score(self) -> float:
        """Calculate quality score (0-100) with bonuses for good fields"""
        base_score = 100.0
        
        # Weight by severity
        weights = {"critical": 20, "warning": 5, "info": 1}
        penalty = sum(weights.get(i.severity, 1) for i in self.issues)
        
        # Apply penalty and bonus
        score = base_score - penalty + self.bonus_points
        
        return max(0.0, min(100.0, score))


class CardValidator:
    """Validates knowledge cards against schema and quality rules"""
    
    def __init__(self, schema_path: str = None):
        self.schema = self._load_schema(schema_path) if schema_path else None
    
    def _load_schema(self, path: str) -> dict:
        """Load schema definition (placeholder for future use)"""
        return {}
    
    def _is_garbage_title(self, title: str) -> bool:
        """Check if title appears to be garbage/corrupted"""
        if not title:
            return False
        return title_is_placeholder(title)

    def fix_card(self, card: dict) -> Tuple[dict, Dict]:
        """Clean a single knowledge card and return change metadata."""
        return clean_card(card)

    def fix_directory(self, cards_dir: str, dry_run: bool = False) -> Dict:
        """Clean all cards in a directory tree."""
        cards_path = Path(cards_dir)
        changed_files = 0
        field_change_counts: Dict[str, int] = {}
        file_changes: List[Dict[str, object]] = []

        for json_file in cards_path.rglob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    card = json.load(f)

                cleaned_card, report = self.fix_card(card)
                changed_fields = report.get("changed_fields", [])
                if not changed_fields:
                    continue

                changed_files += 1
                for field_name in changed_fields:
                    field_change_counts[field_name] = field_change_counts.get(field_name, 0) + 1

                file_changes.append(
                    {
                        "card_id": cleaned_card.get("card_id", json_file.stem),
                        "path": str(json_file),
                        "changed_fields": changed_fields,
                    }
                )

                if not dry_run:
                    with open(json_file, "w", encoding="utf-8") as f:
                        json.dump(cleaned_card, f, ensure_ascii=False, indent=2)

            except Exception as e:
                file_changes.append(
                    {
                        "card_id": json_file.stem,
                        "path": str(json_file),
                        "error": str(e),
                    }
                )

        return {
            "changed_files": changed_files,
            "field_change_counts": field_change_counts,
            "file_changes": file_changes,
            "dry_run": dry_run,
        }
    
    def validate_card(self, card: dict) -> ValidationResult:
        """Validate a single knowledge card"""
        result = ValidationResult(
            card_id=card.get("card_id", "UNKNOWN"),
            source_type=card.get("source_type", "unknown"),
            source_file=card.get("source_file", "")
        )
        
        source_type = card.get("source_type", "unknown")
        
        # 1. Check required fields
        for field in REQUIRED_FIELDS.get(source_type, []):
            if field not in card:
                result.issues.append(CardIssue(
                    card_id=result.card_id,
                    field=field,
                    issue_type="missing",
                    severity="critical",
                    message=f"Required field '{field}' is missing"
                ))
            elif not card.get(field):
                result.issues.append(CardIssue(
                    card_id=result.card_id,
                    field=field,
                    issue_type="empty",
                    severity="critical" if field in ["card_id", "source_type"] else "warning",
                    message=f"Required field '{field}' is empty"
                ))
        
        # 2. Check recommended fields
        for field in RECOMMENDED_FIELDS.get(source_type, []):
            if field not in card or not card.get(field):
                result.issues.append(CardIssue(
                    card_id=result.card_id,
                    field=field,
                    issue_type="empty",
                    severity="warning",
                    message=f"Recommended field '{field}' is missing or empty",
                    suggestion=f"Consider adding {field} for better quality"
                ))
        
        # 3. Check title quality
        title = card.get("title", "")
        cleaned_title = clean_title(title, card.get("source_file", ""))
        
        # 文章类型标签黑名单（这些不是真正的标题）
        article_type_labels = [
            "review article", "original article", "research article",
            "short communication", "case report", "editorial",
            "letter to editor", "commentary", "perspective",
            "original research", "brief communication",
            "access this article online", "quick response code",
            # 新增
            "from cas & cae members", "cas & cae members",
            "selected by", "recommended by",
            "research paper", "full paper", "extended abstract",
            "position paper", "white paper", "technical report"
        ]
        
        if not title:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="title",
                issue_type="empty",
                severity="critical",
                message="Title is empty - this will hurt retrieval quality",
                suggestion="Extract title from PDF filename or first page"
            ))
        elif title.lower() in article_type_labels:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="title",
                issue_type="article_type_label",
                severity="critical",
                message=f"Title is an article type label: '{title}' - NOT a real title",
                suggestion="Extract the actual paper title from the document"
            ))
        elif self._is_garbage_title(title):
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="title",
                issue_type="garbage",
                severity="critical",
                message=f"Title appears to be garbage/corrupted: '{title[:50]}...'",
                suggestion=f"Replace with cleaned fallback title: '{cleaned_title}'"
            ))
        elif cleaned_title and cleaned_title != title:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="title",
                issue_type="needs_cleaning",
                severity="warning",
                message=f"Title should be normalized to '{cleaned_title}'",
                suggestion="Run validator with --fix to apply title cleanup"
            ))
        elif title.isupper() and len(title) < 50 and " " in title:
            # 全大写短标题可能是文章类型标签
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="title",
                issue_type="suspected_label",
                severity="warning",
                message=f"Title is all uppercase and short - may be article type label: '{title}'",
                suggestion="Verify this is the actual title, not a section header"
            ))
        elif len(title) < 5:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="title",
                issue_type="low_quality",
                severity="warning",
                message=f"Title too short ({len(title)} chars) - likely incomplete",
                suggestion="Title should be 5-200 characters"
            ))
        elif len(title) > 200:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="title",
                issue_type="low_quality",
                severity="info",
                message=f"Title very long ({len(title)} chars) - may need truncation",
                suggestion="Consider shortening for better display"
            ))
        
        # 4. Check authors quality
        authors = card.get("authors", [])
        cleaned_authors = clean_authors(authors, source_file=card.get("source_file", ""), title=cleaned_title or title)
        
        # 扩展的通用占位作者
        generic_author_lists = [
            [], ["CNKI"], ["Unknown"], ["PDF"], ["未知"], ["佚名"],
            ["Administrator"], ["administrator"], ["Admin"], ["admin"],
            ["Author"], ["USER"], ["Guest"], ["System"], ["Test"]
        ]
        
        # 单个占位作者（需要特殊处理）
        single_placeholder_authors = [
            "CNKI", "Unknown", "PDF", "未知", "佚名",
            "Administrator", "administrator", "Admin", "admin",
            "Author", "USER", "Guest", "System", "Test"
        ]
        
        # 机构/地址词汇（不应出现在作者列表中）
        institution_words = {
            "university", "college", "institute", "hospital", "school",
            "department", "center", "laboratory", "faculty",
            "beijing", "shanghai", "china", "chinese",
            "access", "article", "online", "website", "correspondence"
        }
        
        if not authors:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="authors",
                issue_type="empty",
                severity="warning",
                message="Authors field is empty",
                suggestion="Extract actual author names from the document"
            ))
        elif authors in generic_author_lists or (len(authors) == 1 and authors[0] in single_placeholder_authors):
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="authors",
                issue_type="low_quality",
                severity="warning",
                message=f"Authors field contains generic placeholder: {authors}",
                suggestion="Extract actual author names from the document"
            ))
        else:
            # 检查作者是否包含机构词汇
            suspicious_authors = []
            for author in authors:
                author_lower = author.lower()
                for word in institution_words:
                    if word in author_lower:
                        suspicious_authors.append(author)
                        break
            
            if suspicious_authors:
                result.issues.append(CardIssue(
                    card_id=result.card_id,
                    field="authors",
                    issue_type="institution_in_authors",
                    severity="warning",
                    message=f"Authors contain institution/address words: {suspicious_authors[:3]}",
                    suggestion="Remove institution names, keep only author names"
                ))

        if cleaned_authors != authors:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="authors",
                issue_type="needs_cleaning",
                severity="warning",
                message=f"Authors should be cleaned to: {cleaned_authors}",
                suggestion="Run validator with --fix to remove institution/email noise"
            ))
        
        # 5. Check page_info field
        page_info = card.get("page_info", {})
        if not page_info:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="page_info",
                issue_type="missing",
                severity="warning",
                message="page_info field is missing",
                suggestion="Add page_info with total_pages, start_page, end_page"
            ))
        else:
            total_pages = page_info.get("total_pages", 0)
            if total_pages <= 0:
                result.issues.append(CardIssue(
                    card_id=result.card_id,
                    field="page_info",
                    issue_type="low_quality",
                    severity="warning",
                    message="page_info.total_pages is 0 or missing",
                    suggestion="Set total_pages to the actual page count"
                ))
        
        # 6. Check knowledge_points quality
        knowledge_points = card.get("knowledge_points", [])
        generic_kp_count = 0
        specific_kp_count = 0
        if knowledge_points:
            for kp in knowledge_points:
                content = kp.get("content", "")
                if is_generic_knowledge_point(content):
                    generic_kp_count += 1
                    result.issues.append(CardIssue(
                        card_id=result.card_id,
                        field="knowledge_points",
                        issue_type="low_quality",
                        severity="warning",
                        message=f"Generic knowledge point: '{content[:50]}...'",
                        suggestion="Replace with specific insights from the document"
                    ))
                else:
                    specific_kp_count += 1
            
            # Report ratio of specific vs generic
            if generic_kp_count > 0 and specific_kp_count == 0:
                result.issues.append(CardIssue(
                    card_id=result.card_id,
                    field="knowledge_points",
                    issue_type="low_quality",
                    severity="warning",
                    message=f"All {generic_kp_count} knowledge points are generic templates",
                    suggestion="Replace with specific insights extracted from the document"
                ))
        else:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="knowledge_points",
                issue_type="empty",
                severity="warning",
                message="No knowledge points extracted"
            ))

        cleaned_card, cleaned_report = self.fix_card(card)
        if cleaned_report.get("changed_fields"):
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="card",
                issue_type="needs_cleaning",
                severity="info",
                message=f"Auto-cleaner would update fields: {', '.join(cleaned_report['changed_fields'])}",
                suggestion="Run validator with --fix to apply safe in-place cleanup"
            ))
        
        # 6.5. Calculate bonus points for good quality fields
        bonus = 0.0
        
        # Bonus for good title (5-200 chars)
        title = card.get("title", "")
        if 5 <= len(title) <= 200:
            bonus += 2.0
        
        # Bonus for non-generic authors
        authors = card.get("authors", [])
        generic_authors = [["CNKI"], ["Unknown"], ["PDF"], ["未知"], ["佚名"], []]
        if authors and authors not in generic_authors:
            bonus += 2.0
        
        # Bonus for valid page_info
        page_info = card.get("page_info", {})
        if page_info and page_info.get("total_pages", 0) > 0:
            bonus += 1.0
        
        # Bonus for specific knowledge points
        if specific_kp_count > 0:
            bonus += min(3.0, specific_kp_count * 0.5)  # Up to 3 points for specific KPs
        
        result.bonus_points = bonus
        
        # 7. Check evidence_sentences quality
        evidence_sentences = card.get("evidence_sentences", [])
        if evidence_sentences:
            for es in evidence_sentences:
                sentence = es.get("sentence", "")
                # Check for irrelevant content
                irrelevant_patterns = [
                    "Foundation of China",
                    "Science Foundation",
                    "supported by",
                    "funded by",
                    "No.",
                    "grant"
                ]
                for pattern in irrelevant_patterns:
                    if pattern.lower() in sentence.lower():
                        result.issues.append(CardIssue(
                            card_id=result.card_id,
                            field="evidence_sentences",
                            issue_type="low_quality",
                            severity="info",
                            message=f"Evidence sentence appears to be funding info: '{sentence[:50]}...'",
                            suggestion="Remove funding statements from evidence_sentences"
                        ))
                        break
        
        # 8. Check citation fields
        citations = card.get("citations", [])
        cross_refs = card.get("cross_references", [])
        
        if not citations:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="citations",
                issue_type="empty",
                severity="info",
                message="No citations extracted - this field is defined but rarely populated",
                suggestion="Consider extracting direct quotes with page numbers"
            ))
        
        if not cross_refs:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="cross_references",
                issue_type="empty",
                severity="info",
                message="No cross-references - cards are not linked to related content"
            ))
        
        # 9. Check for personality-related content
        if source_type == "clinical_experience":
            clinical_insights = card.get("clinical_insights", "")
            if clinical_insights and len(clinical_insights) > 100:
                pass  # Good - has substantial clinical insights
            elif not clinical_insights:
                result.issues.append(CardIssue(
                    card_id=result.card_id,
                    field="clinical_insights",
                    issue_type="empty",
                    severity="warning",
                    message="No clinical insights - missing personality content",
                    suggestion="Extract professor's clinical reasoning and insights"
                ))
        
        # 10. Check related fields
        related_constitutions = card.get("related_constitutions", [])
        related_diseases = card.get("related_diseases", [])
        
        if not related_constitutions and not related_diseases:
            result.issues.append(CardIssue(
                card_id=result.card_id,
                field="related_fields",
                issue_type="empty",
                severity="warning",
                message="No related constitutions or diseases - poor categorization",
                suggestion="Extract related TCM constitution types and diseases"
            ))
        
        return result
    
    def validate_directory(self, cards_dir: str) -> List[ValidationResult]:
        """Validate all cards in a directory"""
        results = []
        cards_path = Path(cards_dir)
        
        for json_file in cards_path.rglob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    card = json.load(f)
                result = self.validate_card(card)
                results.append(result)
            except json.JSONDecodeError as e:
                results.append(ValidationResult(
                    card_id=json_file.stem,
                    source_type="unknown",
                    source_file=str(json_file),
                    issues=[CardIssue(
                        card_id=json_file.stem,
                        field="file",
                        issue_type="format_error",
                        severity="critical",
                        message=f"JSON parse error: {e}"
                    )]
                ))
            except Exception as e:
                results.append(ValidationResult(
                    card_id=json_file.stem,
                    source_type="unknown",
                    source_file=str(json_file),
                    issues=[CardIssue(
                        card_id=json_file.stem,
                        field="file",
                        issue_type="format_error",
                        severity="critical",
                        message=f"Error reading file: {e}"
                    )]
                ))
        
        return results


def print_report(results: List[ValidationResult], verbose: bool = False):
    """Print validation report"""
    print("=" * 70)
    print("Knowledge Card Quality Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    # Summary
    total = len(results)
    valid = sum(1 for r in results if r.is_valid)
    invalid = total - valid
    
    avg_quality = sum(r.quality_score for r in results) / total if total > 0 else 0
    avg_bonus = sum(r.bonus_points for r in results) / total if total > 0 else 0
    
    print(f"Total cards: {total}")
    print(f"Valid cards: {valid} ({valid/total*100:.1f}%)")
    print(f"Invalid cards: {invalid} ({invalid/total*100:.1f}%)")
    print(f"Average quality score: {avg_quality:.1f}/100")
    print(f"Average bonus points: {avg_bonus:.1f}")
    print()
    
    # Issue breakdown by severity
    issues_by_severity = {"critical": 0, "warning": 0, "info": 0}
    issues_by_type = {}
    issues_by_field = {}
    
    for r in results:
        for issue in r.issues:
            issues_by_severity[issue.severity] = issues_by_severity.get(issue.severity, 0) + 1
            issues_by_type[issue.issue_type] = issues_by_type.get(issue.issue_type, 0) + 1
            issues_by_field[issue.field] = issues_by_field.get(issue.field, 0) + 1
    
    print("Issues by severity:")
    for severity, count in issues_by_severity.items():
        print(f"  {severity}: {count}")
    print()
    
    print("Issues by type:")
    for issue_type, count in sorted(issues_by_type.items(), key=lambda x: -x[1]):
        print(f"  {issue_type}: {count}")
    print()
    
    print("Issues by field (top 10):")
    for field, count in sorted(issues_by_field.items(), key=lambda x: -x[1])[:10]:
        print(f"  {field}: {count}")
    print()
    
    # Cards with most issues
    print("Cards with most issues:")
    sorted_results = sorted(results, key=lambda r: len(r.issues), reverse=True)
    for r in sorted_results[:5]:
        if r.issues:
            print(f"  {r.card_id}: {len(r.issues)} issues (quality: {r.quality_score:.0f}, bonus: {r.bonus_points:.1f})")
    print()
    
    # Cards with highest quality
    print("Cards with highest quality:")
    sorted_by_quality = sorted(results, key=lambda r: r.quality_score, reverse=True)
    for r in sorted_by_quality[:5]:
        print(f"  {r.card_id}: quality {r.quality_score:.0f} (bonus: {r.bonus_points:.1f})")
    print()
    
    # Detailed issues for invalid cards
    if verbose:
        print("=" * 70)
        print("Detailed Issues")
        print("=" * 70)
        
        for r in results:
            if not r.is_valid:
                print(f"\n[{r.card_id}] {r.source_file}")
                for issue in r.issues:
                    if issue.severity in ["critical", "warning"]:
                        print(f"  [{issue.severity}] {issue.field}: {issue.message}")
                        if issue.suggestion:
                            print(f"    Suggestion: {issue.suggestion}")


def print_fix_summary(fix_report: Dict):
    """Print auto-clean summary."""
    action = "Would update" if fix_report.get("dry_run") else "Updated"
    print("=" * 70)
    print("Auto-Clean Summary")
    print("=" * 70)
    print(f"{action} files: {fix_report.get('changed_files', 0)}")

    field_change_counts = fix_report.get("field_change_counts", {})
    if field_change_counts:
        print("Changed fields:")
        for field_name, count in sorted(field_change_counts.items(), key=lambda x: -x[1]):
            print(f"  {field_name}: {count}")
    print()


def save_report(results: List[ValidationResult], output_path: str):
    """Save report to JSON file"""
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_cards": len(results),
            "valid_cards": sum(1 for r in results if r.is_valid),
            "invalid_cards": sum(1 for r in results if not r.is_valid),
            "average_quality": sum(r.quality_score for r in results) / len(results) if results else 0,
            "average_bonus": sum(r.bonus_points for r in results) / len(results) if results else 0
        },
        "cards": [
            {
                "card_id": r.card_id,
                "source_type": r.source_type,
                "source_file": r.source_file,
                "is_valid": r.is_valid,
                "quality_score": r.quality_score,
                "bonus_points": r.bonus_points,
                "issues": [
                    {
                        "field": i.field,
                        "issue_type": i.issue_type,
                        "severity": i.severity,
                        "message": i.message,
                        "suggestion": i.suggestion
                    }
                    for i in r.issues
                ]
            }
            for r in results
        ]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Validate knowledge cards")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Cards directory")
    parser.add_argument("--report", "-r", help="Save report to JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed issues")
    parser.add_argument("--fix", action="store_true", help="Apply safe in-place cleanup to knowledge cards")
    parser.add_argument("--dry-run", action="store_true", help="Preview cleanup changes without writing files")
    
    args = parser.parse_args()
    
    # Resolve path - try multiple strategies
    cards_dir = Path(args.cards)
    
    # Strategy 1: If absolute path, use directly
    if cards_dir.is_absolute():
        pass
    # Strategy 2: Try from current working directory first
    elif cards_dir.exists():
        cards_dir = cards_dir.resolve()
    # Strategy 3: Try from script's parent directory
    else:
        script_dir = Path(__file__).parent
        relative_to_script = script_dir.parent / cards_dir
        if relative_to_script.exists():
            cards_dir = relative_to_script.resolve()
        else:
            # Keep original for error message
            cards_dir = cards_dir.resolve()
    
    if not cards_dir.exists():
        print(f"Error: Cards directory not found: {cards_dir}")
        print(f"  Current working directory: {Path.cwd()}")
        print(f"  Script directory: {Path(__file__).parent}")
        print(f"  Tried paths:")
        print(f"    - {Path(args.cards).resolve()}")
        print(f"    - {Path(__file__).parent.parent / args.cards}")
        sys.exit(1)
    
    # Validate
    validator = CardValidator()

    if args.fix or args.dry_run:
        fix_report = validator.fix_directory(str(cards_dir), dry_run=args.dry_run)
        print_fix_summary(fix_report)

    results = validator.validate_directory(str(cards_dir))
    
    # Print report
    print_report(results, verbose=args.verbose)
    
    # Save report if requested
    if args.report:
        save_report(results, args.report)
    
    # Exit with error code if any critical issues
    has_critical = any(not r.is_valid for r in results)
    sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()
