import { describe, it, expect } from 'vitest';
import { getWantToRead, getShelf, countReadLastYear, resolveBook, STATUS } from './client';

const hasToken = !!process.env.HARDCOVER_TOKEN;

describe.skipIf(!hasToken)('Hardcover API integration (read-only)', () => {
  it('getWantToRead returns an array of user books', async () => {
    const items = await getWantToRead(5);
    expect(Array.isArray(items)).toBe(true);
    for (const item of items) {
      expect(item.book).toBeDefined();
      expect(typeof item.book.id).toBe('number');
      expect(typeof item.book.title).toBe('string');
    }
  });

  it('getShelf(READ) returns books with status_id 3', async () => {
    const items = await getShelf(STATUS.READ, 5);
    expect(Array.isArray(items)).toBe(true);
    for (const item of items) {
      expect(item.status_id).toBe(STATUS.READ);
      expect(item.book).toBeDefined();
      expect(typeof item.book.title).toBe('string');
    }
  });

  it('countReadLastYear returns year, count, and sample', async () => {
    const result = await countReadLastYear();
    expect(typeof result.year).toBe('number');
    expect(typeof result.count).toBe('number');
    expect(Array.isArray(result.sample)).toBe(true);
    expect(result.year).toBe(new Date().getUTCFullYear() - 1);
  });

  it('resolveBook finds a well-known title', async () => {
    const result = await resolveBook('Dune');
    expect(result.kind).not.toBe('none');
    if (result.kind === 'exact') {
      expect(result.book.title.toLowerCase()).toContain('dune');
    } else if (result.kind === 'ambiguous') {
      expect(result.matches.length).toBeGreaterThan(1);
    }
  });

  it('resolveBook returns none for a nonsense title', async () => {
    const result = await resolveBook('xyzzy_nonexistent_book_12345_qqq');
    expect(result.kind).toBe('none');
  });
});
