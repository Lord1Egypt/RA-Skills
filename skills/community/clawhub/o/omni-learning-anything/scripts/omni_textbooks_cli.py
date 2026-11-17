"""Discover a textbook, acquire one copy and bind learning to its source."""
from pathlib import Path


def configure(subcommands):
    parser = subcommands.add_parser('textbooks', help='Discover and use K–12 textbooks')
    actions = parser.add_subparsers(dest='textbook_action', required=True)
    actions.add_parser('catalog')
    search = actions.add_parser('resolve')
    search.add_argument('--query', required=True)
    for name in ('grade', 'subject', 'edition', 'volume', 'year', 'school-system', 'stage', 'book-id'):
        search.add_argument('--' + name)
    search.add_argument('--allow-default', action='store_true')
    for action in ('show', 'acquire', 'bind', 'figure', 'ocr'):
        actions.add_parser(action).add_argument('--book', required=True)
    acquire = actions.choices['acquire']
    acquire.add_argument('--local-pdf', type=Path)
    acquire.add_argument('--confirm-local-edition', action='store_true')
    acquire.add_argument('--retry', action='store_true')
    for action in ('bind', 'figure', 'ocr'):
        actions.choices[action].add_argument('--sha256', required=True)
    ocr = actions.choices['ocr']
    ocr.add_argument('--material-id', required=True)
    ocr.add_argument('--pages', required=True)
    bind = actions.choices['bind']
    bind.add_argument('--material-id', required=True)
    bind.add_argument('--pages', required=True)
    bind.add_argument('--focus', required=True)
    figure = actions.choices['figure']
    figure.add_argument('--page', type=int, required=True)
    figure.add_argument('--box', type=float, nargs=4, required=True, metavar=('X0', 'Y0', 'X1', 'Y1'))
    figure.add_argument('--caption', required=True)
    locate = actions.add_parser('locate')
    locate.add_argument('--material-id', required=True)
    locate.add_argument('--sha256', required=True)
    locate.add_argument('--query', required=True)


def execute(root, args):
    from omni_textbook_index import catalog, get, resolve

    action = args.textbook_action
    if action == 'catalog':
        data = catalog()
        return {key: value for key, value in data.items() if key != 'books'} | {
            'book_count': len(data['books']),
            'subjects_by_stage': {stage: sorted({book['subject'] for book in data['books']
                                                 if book['stage'] == stage and book.get('subject')})
                                  for stage in sorted({book['stage'] for book in data['books']})},
        }
    if action == 'resolve':
        return resolve(args.query, grade=args.grade, subject=args.subject, edition=args.edition, volume=args.volume,
                       year=args.year, school_system=args.school_system, stage=args.stage,
                       book_id=args.book_id, allow_default=args.allow_default)
    if action == 'locate':
        from omni_textbooks import locate
        return locate(root, args.material_id, args.sha256, args.query)
    book = get(args.book)
    if action == 'show':
        return book
    if action == 'acquire':
        from omni_textbook_fetch import acquire
        return acquire(root, book, local_pdf=args.local_pdf, confirm_local_edition=args.confirm_local_edition,
                       retry=args.retry)
    if action == 'ocr':
        from omni_textbook_ocr import ocr
        return ocr(root, book['book_id'], args.material_id, args.sha256, args.pages)
    if action == 'bind':
        from omni_textbooks import bind
        return bind(root, book, args.material_id, args.sha256, args.pages, args.focus)
    from omni_textbooks import extract_figure
    return extract_figure(root, book, args.sha256, args.page, args.box, args.caption)
