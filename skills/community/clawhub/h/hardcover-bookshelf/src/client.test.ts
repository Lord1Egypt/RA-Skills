import { describe, it, expect, vi, beforeEach } from 'vitest';
import { normalizeTitle, authorLabel, formatBookLine, formatUserBookLine } from './client';
import type { Book, UserBook } from './types';

describe('normalizeTitle', () => {
  it('lowercases input', () => {
    expect(normalizeTitle('The Great Gatsby')).toBe('the great gatsby');
  });

  it('strips punctuation and replaces with spaces', () => {
    expect(normalizeTitle('The Complete "Maus"')).toBe('the complete maus');
  });

  it('handles colons, semicolons, and other punctuation', () => {
    expect(normalizeTitle("Harry Potter: The Boy Who Lived!")).toBe('harry potter the boy who lived');
  });

  it('collapses multiple spaces', () => {
    expect(normalizeTitle('a   b   c')).toBe('a b c');
  });

  it('trims whitespace', () => {
    expect(normalizeTitle('  hello  ')).toBe('hello');
  });

  it('handles brackets and parentheses', () => {
    expect(normalizeTitle('Title [Special Edition] (2024)')).toBe('title special edition 2024');
  });

  it('handles empty string', () => {
    expect(normalizeTitle('')).toBe('');
  });
});

describe('authorLabel', () => {
  it('returns comma-joined author names', () => {
    const book: Book = {
      id: 1,
      title: 'Test',
      cached_contributors: [
        { author: { name: 'Alice' } },
        { author: { name: 'Bob' } },
      ],
    };
    expect(authorLabel(book)).toBe('Alice, Bob');
  });

  it('limits to 3 authors', () => {
    const book: Book = {
      id: 1,
      title: 'Test',
      cached_contributors: [
        { author: { name: 'A' } },
        { author: { name: 'B' } },
        { author: { name: 'C' } },
        { author: { name: 'D' } },
      ],
    };
    expect(authorLabel(book)).toBe('A, B, C');
  });

  it('returns empty string when no contributors', () => {
    const book: Book = { id: 1, title: 'Test', cached_contributors: [] };
    expect(authorLabel(book)).toBe('');
  });

  it('returns empty string when cached_contributors is undefined', () => {
    const book: Book = { id: 1, title: 'Test' };
    expect(authorLabel(book)).toBe('');
  });

  it('filters out entries with missing author name', () => {
    const book: Book = {
      id: 1,
      title: 'Test',
      cached_contributors: [
        { author: { name: 'Alice' } },
        { author: {} },
        { author: { name: 'Bob' } },
      ],
    };
    expect(authorLabel(book)).toBe('Alice, Bob');
  });
});

describe('formatBookLine', () => {
  it('formats book with author and year', () => {
    const book: Book = {
      id: 1,
      title: 'Dune',
      release_year: 1965,
      cached_contributors: [{ author: { name: 'Frank Herbert' } }],
    };
    expect(formatBookLine(book)).toBe('Dune (1965) — Frank Herbert');
  });

  it('formats book with author but no year', () => {
    const book: Book = {
      id: 1,
      title: 'Dune',
      cached_contributors: [{ author: { name: 'Frank Herbert' } }],
    };
    expect(formatBookLine(book)).toBe('Dune — Frank Herbert');
  });

  it('formats book with year but no author', () => {
    const book: Book = {
      id: 1,
      title: 'Dune',
      release_year: 1965,
      cached_contributors: [],
    };
    expect(formatBookLine(book)).toBe('Dune (1965)');
  });

  it('formats book with neither author nor year', () => {
    const book: Book = { id: 1, title: 'Dune' };
    expect(formatBookLine(book)).toBe('Dune');
  });
});

describe('formatUserBookLine', () => {
  it('delegates to formatBookLine', () => {
    const userBook: UserBook = {
      id: 1,
      book: {
        id: 1,
        title: 'Dune',
        release_year: 1965,
        cached_contributors: [{ author: { name: 'Frank Herbert' } }],
      },
    };
    expect(formatUserBookLine(userBook)).toBe('Dune (1965) — Frank Herbert');
  });
});

describe('resolveBook', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
    process.env.HARDCOVER_TOKEN = 'Bearer test-token';
  });

  it('returns exact match from currently-reading shelf', async () => {
    const { resolveBook } = await import('./client');
    const mockFetch = vi.mocked(fetch);

    // First call: getShelf (currently reading)
    mockFetch.mockResolvedValueOnce(new Response(JSON.stringify({
      data: {
        me: [{
          user_books: [{
            id: 1,
            status_id: 2,
            book: { id: 42, title: 'Dune', release_year: 1965, cached_contributors: [] },
          }],
        }],
      },
    })));

    const result = await resolveBook('Dune');
    expect(result.kind).toBe('exact');
    if (result.kind === 'exact') {
      expect(result.book.id).toBe(42);
      expect(result.book.title).toBe('Dune');
    }
  });

  it('returns none when no results found', async () => {
    const { resolveBook } = await import('./client');
    const mockFetch = vi.mocked(fetch);

    // First call: getShelf (currently reading) - empty
    mockFetch.mockResolvedValueOnce(new Response(JSON.stringify({
      data: { me: [{ user_books: [] }] },
    })));

    // Second call: search - empty
    mockFetch.mockResolvedValueOnce(new Response(JSON.stringify({
      data: { search: { results: { hits: [] } } },
    })));

    const result = await resolveBook('nonexistent book');
    expect(result.kind).toBe('none');
  });

  it('returns ambiguous when multiple matches found', async () => {
    const { resolveBook } = await import('./client');
    const mockFetch = vi.mocked(fetch);

    // First call: getShelf - empty
    mockFetch.mockResolvedValueOnce(new Response(JSON.stringify({
      data: { me: [{ user_books: [] }] },
    })));

    // Second call: search - multiple results with same normalized title
    mockFetch.mockResolvedValueOnce(new Response(JSON.stringify({
      data: {
        search: {
          results: {
            hits: [
              { document: { id: '1', title: 'Dune', release_year: 1965 } },
              { document: { id: '2', title: 'Dune', release_year: 2021 } },
            ],
          },
        },
      },
    })));

    const result = await resolveBook('Dune');
    expect(result.kind).toBe('ambiguous');
    if (result.kind === 'ambiguous') {
      expect(result.matches).toHaveLength(2);
    }
  });
});

describe('getWantToRead', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
    process.env.HARDCOVER_TOKEN = 'Bearer test-token';
  });

  it('parses me[0].user_books correctly', async () => {
    const { getWantToRead } = await import('./client');
    const mockFetch = vi.mocked(fetch);

    mockFetch.mockResolvedValueOnce(new Response(JSON.stringify({
      data: {
        me: [{
          user_books: [
            {
              id: 1,
              date_added: '2026-01-01',
              book: { id: 10, title: 'Book A', release_year: 2020, cached_contributors: [] },
            },
            {
              id: 2,
              date_added: '2026-01-02',
              book: { id: 20, title: 'Book B', release_year: 2021, cached_contributors: [] },
            },
          ],
        }],
      },
    })));

    const result = await getWantToRead(5);
    expect(result).toHaveLength(2);
    expect(result[0].book.title).toBe('Book A');
    expect(result[1].book.title).toBe('Book B');
  });

  it('returns empty array when me is empty', async () => {
    const { getWantToRead } = await import('./client');
    const mockFetch = vi.mocked(fetch);

    mockFetch.mockResolvedValueOnce(new Response(JSON.stringify({
      data: { me: [{}] },
    })));

    const result = await getWantToRead();
    expect(result).toEqual([]);
  });
});
