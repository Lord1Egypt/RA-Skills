#!/usr/bin/env python3
"""Generate placeholder text (Lorem Ipsum and alternatives) for design, development, and testing.

Supports classic Lorem Ipsum, random English sentences, numbered paragraphs, and custom word lists.
Output formats: plain text, HTML, Markdown, JSON.
"""

import argparse
import json
import random
import sys
import textwrap

LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure "
    "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur "
    "excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit "
    "anim id est laborum sed ut perspiciatis unde omnis iste natus error sit voluptatem "
    "accusantium doloremque laudantium totam rem aperiam eaque ipsa quae ab illo inventore "
    "veritatis et quasi architecto beatae vitae dicta sunt explicabo nemo enim ipsam "
    "voluptatem quia voluptas sit aspernatur aut odit aut fugit sed quia consequuntur magni "
    "dolores eos qui ratione voluptatem sequi nesciunt neque porro quisquam est qui dolorem "
    "ipsum quia dolor sit amet consectetur adipisci velit sed quia non numquam eius modi "
    "tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem"
).split()

HIPSTER_WORDS = (
    "artisan craft beer vinyl record aesthetic sustainable organic cold-pressed kombucha "
    "avocado toast gluten-free farm-to-table sriracha heirloom fixie bicycle selfie "
    "authentic retro vintage minimalist curated bespoke handcrafted slow-roasted "
    "pour-over single-origin fair-trade micro-batch small-batch locally-sourced "
    "ethically-made cruelty-free plant-based vegan activated charcoal matcha turmeric "
    "quinoa chia seed acai bowl sourdough fermented probiotic gut-health wellness "
    "mindfulness meditation yoga pilates breathwork journaling gratitude manifestation "
    "crystals sage smudging tarot reading moon phase ritual ceremony intention setting"
).split()

TECH_WORDS = (
    "algorithm microservice kubernetes container docker serverless lambda function "
    "API endpoint REST GraphQL websocket middleware pipeline deployment CI CD "
    "infrastructure terraform ansible provisioning scalability throughput latency "
    "distributed consensus sharding replication failover load-balancer proxy cache "
    "redis memcached queue kafka rabbitmq event-driven webhook callback async await "
    "promise observable reactive stream buffer pipeline ETL data-lake warehouse "
    "schema migration rollback snapshot backup disaster-recovery monitoring alerting "
    "dashboard metrics tracing observability SLO SLA uptime availability resilience"
).split()

WORD_LISTS = {
    "lorem": LOREM_WORDS,
    "hipster": HIPSTER_WORDS,
    "tech": TECH_WORDS,
}

CLASSIC_FIRST = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua."
)


def generate_sentence(words: list[str], min_words: int = 5, max_words: int = 15) -> str:
    length = random.randint(min_words, max_words)
    sentence_words = [random.choice(words) for _ in range(length)]
    sentence_words[0] = sentence_words[0].capitalize()
    return " ".join(sentence_words) + "."


def generate_paragraph(words: list[str], sentences: int = 5) -> str:
    return " ".join(generate_sentence(words) for _ in range(sentences))


def generate_text(
    count: int,
    unit: str,
    style: str,
    classic_start: bool = True,
) -> list[str]:
    words = WORD_LISTS.get(style, LOREM_WORDS)

    if unit == "words":
        all_words = [random.choice(words) for _ in range(count)]
        if classic_start and style == "lorem" and count >= 5:
            classic = CLASSIC_FIRST.rstrip(".").split()[:count]
            for i, w in enumerate(classic):
                all_words[i] = w
        return [" ".join(all_words)]

    if unit == "sentences":
        results = []
        for i in range(count):
            if i == 0 and classic_start and style == "lorem":
                results.append(CLASSIC_FIRST)
            else:
                results.append(generate_sentence(words))
        return results

    # paragraphs
    results = []
    for i in range(count):
        if i == 0 and classic_start and style == "lorem":
            para = CLASSIC_FIRST + " " + generate_paragraph(words, sentences=4)
        else:
            para = generate_paragraph(words, sentences=random.randint(4, 7))
        results.append(para)
    return results


def format_output(paragraphs: list[str], fmt: str, unit: str) -> str:
    if fmt == "json":
        if unit == "words":
            return json.dumps({"text": paragraphs[0]}, indent=2)
        return json.dumps({"paragraphs": paragraphs}, indent=2)

    if fmt == "html":
        if unit == "words":
            return f"<p>{paragraphs[0]}</p>"
        return "\n\n".join(f"<p>{p}</p>" for p in paragraphs)

    if fmt == "markdown":
        return "\n\n".join(paragraphs)

    # plain
    return "\n\n".join(paragraphs)


def main():
    parser = argparse.ArgumentParser(
        description="Generate placeholder text (Lorem Ipsum and alternatives).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s                          # 3 paragraphs of Lorem Ipsum
              %(prog)s -n 5 -u sentences        # 5 sentences
              %(prog)s -n 50 -u words           # 50 words
              %(prog)s -s hipster -n 2          # 2 hipster-style paragraphs
              %(prog)s -s tech -f html          # tech jargon in HTML
              %(prog)s -n 1 -f json             # 1 paragraph as JSON
              %(prog)s --no-classic -n 2        # skip classic opening
        """),
    )
    parser.add_argument(
        "-n", "--count", type=int, default=3,
        help="Number of units to generate (default: 3)",
    )
    parser.add_argument(
        "-u", "--unit", choices=["paragraphs", "sentences", "words"], default="paragraphs",
        help="Unit type (default: paragraphs)",
    )
    parser.add_argument(
        "-s", "--style", choices=list(WORD_LISTS.keys()), default="lorem",
        help="Word style (default: lorem)",
    )
    parser.add_argument(
        "-f", "--format", choices=["plain", "html", "markdown", "json"], default="plain",
        dest="fmt",
        help="Output format (default: plain)",
    )
    parser.add_argument(
        "--no-classic", action="store_true",
        help="Skip the classic 'Lorem ipsum dolor sit amet...' opening",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducible output",
    )

    args = parser.parse_args()

    if args.count < 1:
        print("Error: count must be at least 1", file=sys.stderr)
        sys.exit(1)

    if args.seed is not None:
        random.seed(args.seed)

    paragraphs = generate_text(
        count=args.count,
        unit=args.unit,
        style=args.style,
        classic_start=not args.no_classic,
    )

    output = format_output(paragraphs, args.fmt, args.unit)
    print(output)


if __name__ == "__main__":
    main()
