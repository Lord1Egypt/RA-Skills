#!/usr/bin/env python3
"""
Nex Decision Journal - Log decisions, track reasoning, review outcomes.
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import sys
import os
import json
import argparse
import datetime as dt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.storage import (
    init_db, save_decision, get_decision, list_decisions,
    update_decision, record_outcome, abandon_decision, delete_decision,
    search_decisions, get_stats, get_all_tags, get_pending_reviews,
    get_lessons, get_overconfident_decisions, get_underconfident_decisions,
    get_accuracy_by_category, get_decisions_by_date_range,
    export_decisions,
)
from lib.config import (
    CATEGORIES, CONFIDENCE_LABELS, CONFIDENCE_MIN, CONFIDENCE_MAX,
    FOLLOW_UP_OPTIONS, DEFAULT_FOLLOW_UP_DAYS,
    STATUS_PENDING, STATUS_REVIEWED, STATUS_ABANDONED,
    ACCURACY_OPTIONS, ACCURACY_CORRECT, ACCURACY_PARTIALLY, ACCURACY_WRONG,
    SEPARATOR, SUBSEPARATOR, MAX_LIST_TITLE_LEN, MAX_LIST_CATEGORY_LEN,
    EXPORT_DIR,
)

FOOTER = "[Decision Journal by Nex AI | nex-ai.be]"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _parse_follow_up(value):
    """Parse follow-up value to ISO date. Accepts: ISO date, shorthand (1w/1m/3m/6m/1y), or int days."""
    if not value:
        return (dt.date.today() + dt.timedelta(days=DEFAULT_FOLLOW_UP_DAYS)).isoformat()

    if value.lower() in FOLLOW_UP_OPTIONS:
        return (dt.date.today() + dt.timedelta(days=FOLLOW_UP_OPTIONS[value.lower()])).isoformat()

    try:
        return (dt.date.today() + dt.timedelta(days=int(value))).isoformat()
    except ValueError:
        pass

    try:
        dt.date.fromisoformat(value)
        return value
    except ValueError:
        pass

    return (dt.date.today() + dt.timedelta(days=DEFAULT_FOLLOW_UP_DAYS)).isoformat()


def _format_date(iso_str):
    """ISO string to YYYY-MM-DD display format."""
    if not iso_str:
        return "N/A"
    try:
        d = dt.date.fromisoformat(iso_str[:10])
        return d.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return iso_str


def _days_ago(iso_str):
    """Days since the given ISO date."""
    if not iso_str:
        return None
    try:
        d = dt.date.fromisoformat(iso_str[:10])
        delta = dt.date.today() - d
        return delta.days
    except (ValueError, TypeError):
        return None


def _days_until(iso_str):
    """Days until the given ISO date."""
    if not iso_str:
        return None
    try:
        d = dt.date.fromisoformat(iso_str[:10])
        delta = d - dt.date.today()
        return delta.days
    except (ValueError, TypeError):
        return None


def _confidence_bar(confidence):
    """Visual confidence bar: [#####.....] 5/10 (Coin flip)."""
    filled = int(confidence)
    empty = CONFIDENCE_MAX - filled
    label = CONFIDENCE_LABELS.get(confidence, "")
    return f"[{'#' * filled}{'.' * empty}] {confidence}/10 ({label})"


def _parse_options(options_str):
    """Parse comma-separated string or JSON array into list."""
    if not options_str:
        return []
    try:
        parsed = json.loads(options_str)
        if isinstance(parsed, list):
            return parsed
    except (json.JSONDecodeError, TypeError):
        pass
    return [o.strip() for o in options_str.split(',') if o.strip()]


def _accuracy_symbol(accuracy):
    """[OK], [~~], or [XX] for prediction accuracy."""
    symbols = {
        ACCURACY_CORRECT: "[OK]",
        ACCURACY_PARTIALLY: "[~~]",
        ACCURACY_WRONG: "[XX]",
    }
    return symbols.get(accuracy, "[??]")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def cmd_log(args):
    """Log a new decision."""
    init_db()

    options_list = None
    if args.options:
        options_list = [o.strip() for o in args.options.split(',')]

    follow_up = _parse_follow_up(args.follow_up)

    confidence = args.confidence
    if confidence < CONFIDENCE_MIN or confidence > CONFIDENCE_MAX:
        print(f"Error: Confidence must be between {CONFIDENCE_MIN} and {CONFIDENCE_MAX}.")
        sys.exit(1)

    category = args.category.lower()
    if category not in CATEGORIES:
        print(f"Warning: '{category}' is not a standard category. Using it anyway.")

    decision_id = save_decision(
        title=args.title,
        context=args.context,
        options=options_list,
        chosen_option=args.chosen,
        reasoning=args.reasoning,
        prediction=args.prediction,
        confidence=confidence,
        category=category,
        tags=args.tags,
        stakes=args.stakes,
        reversible=not args.irreversible,
        follow_up_date=follow_up,
    )

    print(f"\nDecision logged (ID: {decision_id})")
    print(f"  Title: {args.title}")
    print(f"  Category: {category}")
    print(f"  Confidence: {_confidence_bar(confidence)}")
    print(f"  Follow-up: {follow_up}")
    if args.chosen:
        print(f"  Chosen: {args.chosen}")
    if args.prediction:
        print(f"  Prediction: {args.prediction}")
    print(f"\n{FOOTER}")


def cmd_show(args):
    """Print full decision details."""
    init_db()

    dec = get_decision(args.id)
    if not dec:
        print(f"Decision {args.id} not found.")
        return

    days = _days_ago(dec['created_at'])
    days_str = f" ({days} days ago)" if days is not None else ""

    print(f"\n{SEPARATOR}")
    print(f"DECISION #{dec['id']}: {dec['title']}")
    print(f"{SEPARATOR}\n")

    print(f"Status: {dec['status'].upper()}")
    print(f"Category: {dec['category']}")
    print(f"Stakes: {dec['stakes']}")
    print(f"Reversible: {'Yes' if dec['reversible'] else 'No'}")
    print(f"Logged: {_format_date(dec['created_at'])}{days_str}")

    if dec['tags']:
        print(f"Tags: {dec['tags']}")

    if dec['context']:
        print(f"\nContext:")
        print(f"  {dec['context']}")

    if dec['options']:
        options = _parse_options(dec['options'])
        if options:
            print(f"\nOptions considered:")
            for i, opt in enumerate(options, 1):
                marker = " >> " if dec['chosen_option'] and opt == dec['chosen_option'] else "    "
                print(f"  {marker}{i}. {opt}")

    if dec['chosen_option']:
        print(f"\nChosen: {dec['chosen_option']}")

    if dec['reasoning']:
        print(f"\nReasoning:")
        print(f"  {dec['reasoning']}")

    if dec['prediction']:
        print(f"\nPrediction:")
        print(f"  {dec['prediction']}")

    print(f"\nConfidence: {_confidence_bar(dec['confidence'])}")

    if dec['follow_up_date']:
        days_left = _days_until(dec['follow_up_date'])
        if days_left is not None and days_left > 0:
            print(f"Review due: {_format_date(dec['follow_up_date'])} ({days_left} days)")
        elif days_left is not None and days_left <= 0:
            print(f"Review due: {_format_date(dec['follow_up_date'])} (OVERDUE by {abs(days_left)} days)")
        else:
            print(f"Review due: {_format_date(dec['follow_up_date'])}")

    if dec['status'] == STATUS_REVIEWED:
        print(f"\n{SUBSEPARATOR}")
        print(f"OUTCOME")
        print(f"{SUBSEPARATOR}\n")
        print(f"Result: {dec['outcome']}")
        print(f"Recorded: {_format_date(dec['outcome_date'])}")
        if dec['prediction_accuracy']:
            print(f"Prediction accuracy: {_accuracy_symbol(dec['prediction_accuracy'])} {dec['prediction_accuracy']}")
        if dec['outcome_notes']:
            print(f"Notes: {dec['outcome_notes']}")
        if dec['lessons_learned']:
            print(f"\nLessons learned:")
            print(f"  {dec['lessons_learned']}")

    if dec['status'] == STATUS_ABANDONED:
        print(f"\n[ABANDONED]")
        if dec['outcome_notes']:
            print(f"Reason: {dec['outcome_notes']}")

    print(f"\n{FOOTER}")


def cmd_list(args):
    """List decisions."""
    init_db()

    decisions = list_decisions(
        status=args.status,
        category=args.category,
        tags=args.tags,
        limit=args.limit if args.limit else 50,
    )

    if not decisions:
        print("No decisions found.")
        print(FOOTER)
        return

    print(f"\n{'ID':<5} {'Date':<12} {'Title':<{MAX_LIST_TITLE_LEN}} {'Category':<{MAX_LIST_CATEGORY_LEN}} {'Conf':<6} {'Status':<10}")
    print("-" * 95)

    for dec in decisions:
        title = dec['title'][:MAX_LIST_TITLE_LEN - 1]
        cat = dec['category'][:MAX_LIST_CATEGORY_LEN]
        date = _format_date(dec['created_at'])
        conf = f"{dec['confidence']}/10"
        status = dec['status']

        if dec['prediction_accuracy']:
            status = f"{status} {_accuracy_symbol(dec['prediction_accuracy'])}"

        print(f"{dec['id']:<5} {date:<12} {title:<{MAX_LIST_TITLE_LEN}} {cat:<{MAX_LIST_CATEGORY_LEN}} {conf:<6} {status:<10}")

    print(f"\nTotal: {len(decisions)} decisions")
    print(FOOTER)


def cmd_review(args):
    """Record the outcome of a decision."""
    init_db()

    dec = get_decision(args.id)
    if not dec:
        print(f"Decision {args.id} not found.")
        return

    if dec['status'] == STATUS_REVIEWED:
        print(f"Decision {args.id} already has a recorded outcome.")
        print(f"Use 'nex-decision-journal edit {args.id}' to modify it.")
        return

    accuracy = args.accuracy
    if accuracy not in ACCURACY_OPTIONS:
        print(f"Error: accuracy must be one of: {', '.join(ACCURACY_OPTIONS)}")
        sys.exit(1)

    success = record_outcome(
        decision_id=args.id,
        outcome=args.outcome,
        prediction_accuracy=accuracy,
        outcome_notes=args.notes,
        lessons_learned=args.lesson,
    )

    if success:
        print(f"\nOutcome recorded for decision #{args.id}")
        print(f"  Title: {dec['title']}")
        print(f"  Outcome: {args.outcome}")
        print(f"  Prediction was: {_accuracy_symbol(accuracy)} {accuracy}")
        if args.lesson:
            print(f"  Lesson: {args.lesson}")
    else:
        print(f"Failed to record outcome for decision {args.id}.")

    print(f"\n{FOOTER}")


def cmd_pending(args):
    """Show decisions awaiting review."""
    init_db()

    pending = get_pending_reviews()

    if not pending:
        print("No decisions due for review. Nice.")
        print(FOOTER)
        return

    print(f"\nDecisions Due for Review ({len(pending)}):\n")

    for dec in pending:
        days_overdue = abs(_days_until(dec['follow_up_date']) or 0)
        print(f"  [{dec['id']}] {dec['title']}")
        print(f"       Category: {dec['category']} | Confidence: {dec['confidence']}/10")
        print(f"       Logged: {_format_date(dec['created_at'])}")
        print(f"       Review due: {_format_date(dec['follow_up_date'])} (overdue {days_overdue} days)")
        if dec['prediction']:
            print(f"       Prediction: {dec['prediction']}")
        print()

    print(f"Use: nex-decision-journal review <ID> --outcome \"what happened\" --accuracy correct|partially_correct|wrong")
    print(FOOTER)


def cmd_search(args):
    """Search across all decisions."""
    init_db()

    results = search_decisions(args.query)

    if not results:
        print(f"No decisions found matching '{args.query}'")
        print(FOOTER)
        return

    print(f"\nSearch results for '{args.query}' ({len(results)} found):\n")

    for dec in results:
        status_str = dec['status']
        if dec['prediction_accuracy']:
            status_str += f" {_accuracy_symbol(dec['prediction_accuracy'])}"

        print(f"  [{dec['id']}] {dec['title']}")
        print(f"       {dec['category']} | {_format_date(dec['created_at'])} | {status_str}")
        if dec['reasoning']:
            reasoning_preview = dec['reasoning'][:80]
            if len(dec['reasoning']) > 80:
                reasoning_preview += "..."
            print(f"       {reasoning_preview}")
        print()

    print(FOOTER)


def cmd_stats(args):
    """Accuracy, confidence, and volume statistics."""
    init_db()

    stats = get_stats()

    print(f"\n{SEPARATOR}")
    print(f"DECISION JOURNAL STATISTICS")
    print(f"{SEPARATOR}\n")

    print(f"Total decisions: {stats['total']}")
    print(f"  Pending: {stats['pending']}")
    print(f"  Reviewed: {stats['reviewed']}")
    print(f"  Abandoned: {stats['abandoned']}")

    if stats['pending_reviews'] > 0:
        print(f"\n  ** {stats['pending_reviews']} decision(s) due for review **")

    print(f"\nAverage confidence: {stats['avg_confidence']}/10")

    if stats['accuracy']:
        total_reviewed = sum(stats['accuracy'].values())
        print(f"\nPrediction Accuracy ({total_reviewed} reviewed):")
        for acc, count in stats['accuracy'].items():
            pct = (count / total_reviewed * 100) if total_reviewed else 0
            bar = '#' * int(pct / 5)
            print(f"  {_accuracy_symbol(acc)} {acc:<20} {count:>3} ({pct:.0f}%) {bar}")

    if stats['confidence_by_accuracy']:
        print(f"\nAverage Confidence by Accuracy:")
        for acc, avg_conf in stats['confidence_by_accuracy'].items():
            print(f"  {acc:<20} {avg_conf}/10")

    if stats['overconfident_wrong'] > 0:
        print(f"\nOverconfidence alerts: {stats['overconfident_wrong']} times you were 8+/10 confident but wrong")

    if stats['underconfident_correct'] > 0:
        print(f"Underconfidence alerts: {stats['underconfident_correct']} times you were 3-/10 confident but correct")

    if stats['by_category']:
        print(f"\nBy Category:")
        for cat, count in stats['by_category'].items():
            print(f"  {cat:<16} {count}")

    if stats['by_stakes']:
        print(f"\nBy Stakes:")
        for stakes, count in stats['by_stakes'].items():
            print(f"  {stakes:<10} {count}")

    if stats['by_month']:
        print(f"\nDecisions per Month (last 12):")
        for month, count in stats['by_month'].items():
            bar = '#' * count
            print(f"  {month} {bar} ({count})")

    print(f"\n{FOOTER}")


def cmd_reflect(args):
    """Bias detection, accuracy by category, lessons learned."""
    init_db()

    print(f"\n{SEPARATOR}")
    print(f"REFLECTION & INSIGHTS")
    print(f"{SEPARATOR}")

    cat_accuracy = get_accuracy_by_category()
    if cat_accuracy:
        print(f"\nAccuracy by Category:")
        print(f"  {'Category':<16} {'Total':<7} {'Correct':<9} {'Partial':<9} {'Wrong':<7}")
        print(f"  {'-' * 48}")
        for row in cat_accuracy:
            print(f"  {row['category']:<16} {row['total']:<7} {row['correct']:<9} {row['partial']:<9} {row['wrong']:<7}")

    overconf = get_overconfident_decisions()
    if overconf:
        print(f"\nOverconfident Decisions (confidence >= 7, but wrong):")
        for dec in overconf[:5]:
            print(f"  [{dec['id']}] {dec['title']} (confidence: {dec['confidence']}/10)")
            if dec['lessons_learned']:
                print(f"       Lesson: {dec['lessons_learned']}")

    underconf = get_underconfident_decisions()
    if underconf:
        print(f"\nUnderconfident Decisions (confidence <= 4, but correct):")
        for dec in underconf[:5]:
            print(f"  [{dec['id']}] {dec['title']} (confidence: {dec['confidence']}/10)")

    lessons = get_lessons()
    if lessons:
        print(f"\nRecent Lessons Learned:")
        for dec in lessons[:10]:
            print(f"  [{dec['id']}] {dec['title']} ({_format_date(dec['outcome_date'])})")
            print(f"       {dec['lessons_learned']}")
            print()

    if not cat_accuracy and not overconf and not underconf and not lessons:
        print(f"\nNo reviewed decisions yet. Review some outcomes first.")

    print(f"\n{FOOTER}")


def cmd_edit(args):
    """Update fields on an existing decision."""
    init_db()

    dec = get_decision(args.id)
    if not dec:
        print(f"Decision {args.id} not found.")
        return

    updates = {}
    if args.title:
        updates['title'] = args.title
    if args.context:
        updates['context'] = args.context
    if args.reasoning:
        updates['reasoning'] = args.reasoning
    if args.prediction:
        updates['prediction'] = args.prediction
    if args.confidence is not None:
        updates['confidence'] = args.confidence
    if args.category:
        updates['category'] = args.category
    if args.tags:
        updates['tags'] = args.tags
    if args.stakes:
        updates['stakes'] = args.stakes
    if args.follow_up:
        updates['follow_up_date'] = _parse_follow_up(args.follow_up)
    if args.chosen:
        updates['chosen_option'] = args.chosen
    if args.lesson:
        updates['lessons_learned'] = args.lesson

    if not updates:
        print("No updates specified.")
        return

    success = update_decision(args.id, **updates)
    if success:
        print(f"Decision #{args.id} updated.")
        for k, v in updates.items():
            print(f"  {k}: {v}")
    else:
        print(f"Failed to update decision {args.id}.")

    print(f"\n{FOOTER}")


def cmd_abandon(args):
    """Mark a decision as abandoned."""
    init_db()

    dec = get_decision(args.id)
    if not dec:
        print(f"Decision {args.id} not found.")
        return

    success = abandon_decision(args.id, reason=args.reason)
    if success:
        print(f"Decision #{args.id} marked as abandoned.")
        print(f"  Title: {dec['title']}")
        if args.reason:
            print(f"  Reason: {args.reason}")
    else:
        print(f"Failed to abandon decision {args.id}.")

    print(f"\n{FOOTER}")


def cmd_tags(args):
    """List all tags used across decisions."""
    init_db()

    tags = get_all_tags()
    if not tags:
        print("No tags used yet.")
        print(FOOTER)
        return

    print(f"\nAll tags ({len(tags)}):")
    print(f"  {', '.join(tags)}")
    print(f"\n{FOOTER}")


def cmd_export(args):
    """Export decisions to JSON or CSV."""
    init_db()

    data = export_decisions(format_type=args.format, status=args.status)
    if not data:
        print("No decisions to export.")
        return

    output_file = args.output or f"decisions_export.{args.format}"
    output_path = EXPORT_DIR / output_file

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(data)

    print(f"Exported to {output_path}")
    print(FOOTER)


def cmd_timeline(args):
    """Show a timeline of decisions for a date range."""
    init_db()

    end_date = args.end or dt.date.today().isoformat()
    start_date = args.start or (dt.date.today() - dt.timedelta(days=30)).isoformat()

    decisions = get_decisions_by_date_range(start_date, end_date)

    if not decisions:
        print(f"No decisions between {start_date} and {end_date}.")
        print(FOOTER)
        return

    print(f"\nDecision Timeline: {start_date} to {end_date}\n")

    current_month = ""
    for dec in decisions:
        month = dec['created_at'][:7]
        if month != current_month:
            current_month = month
            print(f"\n  {current_month}")
            print(f"  {'-' * 50}")

        status_str = dec['status']
        if dec['prediction_accuracy']:
            status_str = _accuracy_symbol(dec['prediction_accuracy'])

        date = _format_date(dec['created_at'])
        print(f"  {date}  [{dec['id']}] {dec['title'][:45]} ({status_str})")

    print(f"\n{FOOTER}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Nex Decision Journal - Track decisions, reasoning, and outcomes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # LOG
    log_parser = subparsers.add_parser('log', help='Log a new decision')
    log_parser.add_argument('title', help='Decision title (what are you deciding)')
    log_parser.add_argument('--context', '-c', help='Background context for the decision')
    log_parser.add_argument('--options', '-o', help='Options considered (comma-separated)')
    log_parser.add_argument('--chosen', help='Which option you chose')
    log_parser.add_argument('--reasoning', '-r', help='Why you made this choice')
    log_parser.add_argument('--prediction', '-p', help='What you predict will happen')
    log_parser.add_argument('--confidence', type=int, default=5,
                            help=f'Confidence in prediction ({CONFIDENCE_MIN}-{CONFIDENCE_MAX}, default: 5)')
    log_parser.add_argument('--category', default='other',
                            help=f'Category: {", ".join(CATEGORIES[:8])}...')
    log_parser.add_argument('--tags', help='Tags (comma-separated)')
    log_parser.add_argument('--stakes', default='medium',
                            choices=['low', 'medium', 'high', 'critical'],
                            help='Stakes level (default: medium)')
    log_parser.add_argument('--irreversible', action='store_true',
                            help='Mark as irreversible decision')
    log_parser.add_argument('--follow-up', default=None,
                            help='When to review (e.g., 1w, 1m, 3m, 6m, 1y, 90, 2026-07-01)')
    log_parser.set_defaults(func=cmd_log)

    # SHOW
    show_parser = subparsers.add_parser('show', help='Show decision details')
    show_parser.add_argument('id', type=int, help='Decision ID')
    show_parser.set_defaults(func=cmd_show)

    # LIST
    list_parser = subparsers.add_parser('list', help='List decisions')
    list_parser.add_argument('--status', choices=[STATUS_PENDING, STATUS_REVIEWED, STATUS_ABANDONED],
                             help='Filter by status')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--tags', help='Filter by tag')
    list_parser.add_argument('--limit', type=int, default=50, help='Max results')
    list_parser.set_defaults(func=cmd_list)

    # REVIEW
    review_parser = subparsers.add_parser('review', help='Record outcome of a decision')
    review_parser.add_argument('id', type=int, help='Decision ID')
    review_parser.add_argument('--outcome', required=True, help='What actually happened')
    review_parser.add_argument('--accuracy', required=True,
                               choices=ACCURACY_OPTIONS,
                               help='How accurate was your prediction')
    review_parser.add_argument('--notes', help='Additional notes about the outcome')
    review_parser.add_argument('--lesson', help='What you learned from this decision')
    review_parser.set_defaults(func=cmd_review)

    # PENDING
    pending_parser = subparsers.add_parser('pending', help='Show decisions due for review')
    pending_parser.set_defaults(func=cmd_pending)

    # SEARCH
    search_parser = subparsers.add_parser('search', help='Search decisions')
    search_parser.add_argument('query', help='Search query')
    search_parser.set_defaults(func=cmd_search)

    # STATS
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.set_defaults(func=cmd_stats)

    # REFLECT
    reflect_parser = subparsers.add_parser('reflect', help='Show reflection insights')
    reflect_parser.set_defaults(func=cmd_reflect)

    # EDIT
    edit_parser = subparsers.add_parser('edit', help='Edit a decision')
    edit_parser.add_argument('id', type=int, help='Decision ID')
    edit_parser.add_argument('--title', help='New title')
    edit_parser.add_argument('--context', help='New context')
    edit_parser.add_argument('--reasoning', help='New reasoning')
    edit_parser.add_argument('--prediction', help='New prediction')
    edit_parser.add_argument('--confidence', type=int, help='New confidence')
    edit_parser.add_argument('--category', help='New category')
    edit_parser.add_argument('--tags', help='New tags')
    edit_parser.add_argument('--stakes', choices=['low', 'medium', 'high', 'critical'],
                             help='New stakes level')
    edit_parser.add_argument('--follow-up', help='New follow-up date')
    edit_parser.add_argument('--chosen', help='New chosen option')
    edit_parser.add_argument('--lesson', help='Add/update lessons learned')
    edit_parser.set_defaults(func=cmd_edit)

    # ABANDON
    abandon_parser = subparsers.add_parser('abandon', help='Mark decision as abandoned')
    abandon_parser.add_argument('id', type=int, help='Decision ID')
    abandon_parser.add_argument('--reason', help='Why the decision was abandoned')
    abandon_parser.set_defaults(func=cmd_abandon)

    # TAGS
    tags_parser = subparsers.add_parser('tags', help='List all tags')
    tags_parser.set_defaults(func=cmd_tags)

    # EXPORT
    export_parser = subparsers.add_parser('export', help='Export decisions')
    export_parser.add_argument('format', choices=['json', 'csv'], help='Export format')
    export_parser.add_argument('--status', help='Filter by status')
    export_parser.add_argument('--output', help='Output filename')
    export_parser.set_defaults(func=cmd_export)

    # TIMELINE
    timeline_parser = subparsers.add_parser('timeline', help='Show decision timeline')
    timeline_parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    timeline_parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    timeline_parser.set_defaults(func=cmd_timeline)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        return

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
