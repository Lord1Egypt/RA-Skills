import { describe, it, expect } from 'vitest';
import { normalizeNotion } from './normalize-notion.js';

function makeNotionPage(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: 'page-001',
    url: 'https://notion.so/page-001',
    created_time: '2024-01-10T00:00:00Z',
    last_edited_time: '2024-01-12T08:00:00Z',
    properties: {
      Name: { title: [{ plain_text: 'Write API docs' }] },
      Assignee: { people: [{ name: 'Alice', id: 'user-a' }] },
      Due: { date: { start: '2024-02-01' } },
      Status: { status: { name: 'In Progress' } },
    },
    ...overrides,
  };
}

describe('normalizeNotion', () => {
  // ---- 1. Happy path: well-formed Notion page ----
  it('maps a Notion task-database row to a valid ActionItem', () => {
    const result = normalizeNotion([makeNotionPage()]);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.id).toBe('notion:page-001');
    expect(item.sourceType).toBe('notion');
    expect(item.source).toBe('notion');
    expect(item.title).toBe('Write API docs');
    expect(item.owner).toBe('Alice');
    expect(item.dueAt).toBe('2024-02-01');
    expect(item.url).toBe('https://notion.so/page-001');
    expect(item.status).toBe('in_progress');
    expect(item.dedupeKeys).toContain('page-001');
    expect(item.dedupeKeys).toContain('https://notion.so/page-001');
    expect(item.participants).toContain('Alice');
    expect(item.confidence).toBe(1.0);
  });

  // ---- 2. Sparse properties: missing assignee and date ----
  it('handles missing assignee and date with owner=null and dueAt=null', () => {
    const result = normalizeNotion([makeNotionPage({
      properties: {
        Name: { title: [{ plain_text: 'Some task' }] },
        // No Assignee, no Due
      },
    })]);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.owner).toBeNull();
    expect(item.dueAt).toBeNull();
    expect(item.title).toBe('Some task');
    expect(item.participants).toEqual([]);
    expect(item.confidence).toBeLessThan(1.0);
    expect(item.confidence).toBeGreaterThanOrEqual(0.7);
    // Still structurally valid
    expect(item.sourceType).toBe('notion');
    expect(item.dedupeKeys).toContain('page-001');
  });

  // ---- 3. Empty title property ----
  it('handles a page with empty title property gracefully', () => {
    const result = normalizeNotion([makeNotionPage({
      properties: {
        Name: { title: [] },
        Assignee: { people: [{ name: 'Bob' }] },
      },
    })]);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.title).toBe('Untitled');
    expect(item.owner).toBe('Bob');
    expect(item.confidence).toBeLessThan(1.0);
  });

  // ---- 4. Completed status is filtered out ----
  it('skips pages with done/completed status', () => {
    const result = normalizeNotion([makeNotionPage({
      properties: {
        Name: { title: [{ plain_text: 'Finished task' }] },
        Status: { status: { name: 'Done' } },
      },
    })]);

    expect(result).toHaveLength(0);
  });

  // ---- 5. Checked checkbox is filtered out ----
  it('skips pages with a checked completion checkbox', () => {
    const result = normalizeNotion([makeNotionPage({
      properties: {
        Name: { title: [{ plain_text: 'Another finished task' }] },
        Done: { checkbox: true },
      },
    })]);

    expect(result).toHaveLength(0);
  });

  // ---- 6. Unchecked checkbox is included ----
  it('includes pages with unchecked completion checkbox', () => {
    const result = normalizeNotion([makeNotionPage({
      properties: {
        Name: { title: [{ plain_text: 'Pending task' }] },
        Done: { checkbox: false },
        Assignee: { people: [{ name: 'Carol' }] },
      },
    })]);

    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Pending task');
    expect(result[0].status).toBe('open');
  });
});
