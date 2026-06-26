import { countReadLastYear, finishReading, formatBookLine, formatUserBookLine, getWantToRead, resolveBook, startReading } from './client';

function usage(): never {
  console.error(`Usage:
  bun run src/cli.ts list [--limit N] [--json]
  bun run src/cli.ts start --title "Book Title" [--json]
  bun run src/cli.ts finish --title "Book Title" [--json]
  bun run src/cli.ts count-last-year [--json]`);
  process.exit(1);
}

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(name);
  return idx >= 0 ? process.argv[idx + 1] : undefined;
}

function has(name: string): boolean {
  return process.argv.includes(name);
}

function print(data: unknown, human: string) {
  if (has('--json')) {
    console.log(JSON.stringify(data, null, 2));
  } else {
    console.log(human);
  }
}

async function resolveRequiredTitle(): Promise<NonNullable<Awaited<ReturnType<typeof resolveBook>> extends infer R ? R : never>> {
  const title = arg('--title');
  if (!title) usage();
  const resolved = await resolveBook(title);
  if (resolved.kind === 'none') {
    throw new Error(`No Hardcover match found for "${title}".`);
  }
  if (resolved.kind === 'ambiguous') {
    throw new Error(
      `Ambiguous title. Choose one:\n${resolved.matches
        .map((book, i) => `${i + 1}. ${formatBookLine(book)} [id=${book.id}]`)
        .join('\n')}`,
    );
  }
  return resolved;
}

async function main() {
  const cmd = process.argv[2];
  if (!cmd) usage();

  if (cmd === 'list') {
    const limit = Number(arg('--limit') ?? '20');
    const items = await getWantToRead(limit);
    print(
      { count: items.length, items },
      items.length
        ? [`Want to Read (${items.length} shown):`, ...items.map((item, i) => `${i + 1}. ${formatUserBookLine(item)}`)].join('\n')
        : 'Your Want to Read shelf is empty.',
    );
    return;
  }

  if (cmd === 'start') {
    const resolved = await resolveRequiredTitle();
    const record = await startReading(resolved.book);
    print(record, `Done — marked ${formatBookLine(record.book)} as Currently Reading.`);
    return;
  }

  if (cmd === 'finish') {
    const resolved = await resolveRequiredTitle();
    const record = await finishReading(resolved.book);
    print(record, `Done — marked ${formatBookLine(record.book)} as Read (${record.last_read_date ?? 'today'}).`);
    return;
  }

  if (cmd === 'count-last-year') {
    const result = await countReadLastYear();
    const sample = result.sample.slice(0, 5).map((item) => `- ${formatUserBookLine(item)}${item.last_read_date ? ` (${item.last_read_date})` : ''}`);
    print(result, [`You read ${result.count} books in ${result.year}.`, ...sample].join('\n'));
    return;
  }

  usage();
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
