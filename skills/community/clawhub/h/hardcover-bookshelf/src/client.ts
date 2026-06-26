import type { Book, SearchHit, UserBook } from './types';

const ENDPOINT = 'https://api.hardcover.app/v1/graphql';

export const STATUS = {
  WANT_TO_READ: 1,
  CURRENTLY_READING: 2,
  READ: 3,
  PAUSED: 4,
  DID_NOT_FINISH: 5,
  IGNORED: 6,
} as const;

function getToken(): string {
  const token = process.env.HARDCOVER_TOKEN?.trim();
  if (!token) {
    throw new Error('HARDCOVER_TOKEN is missing. Expected the full header value copied from Hardcover, e.g. "Bearer eyJ..."');
  }
  if (!token.startsWith('Bearer ')) {
    throw new Error('HARDCOVER_TOKEN must include the literal "Bearer " prefix, because Hardcover shows the full auth header value on the API page.');
  }
  return token;
}

async function graphql<T>(query: string, variables?: Record<string, unknown>): Promise<T> {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: getToken(),
    },
    body: JSON.stringify({ query, variables }),
  });

  const text = await res.text();
  let payload: any;
  try {
    payload = JSON.parse(text);
  } catch {
    throw new Error(`Hardcover returned non-JSON response (${res.status}): ${text.slice(0, 300)}`);
  }

  if (!res.ok) {
    throw new Error(`Hardcover HTTP ${res.status}: ${JSON.stringify(payload)}`);
  }
  if (payload.errors?.length) {
    throw new Error(`Hardcover GraphQL error: ${payload.errors.map((e: any) => e.message).join('; ')}`);
  }
  return payload.data as T;
}

export function normalizeTitle(input: string): string {
  return input
    .toLowerCase()
    .replace(/["'’:;,.!?()[\]{}]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function authorLabel(book: Book): string {
  const authors = (book.cached_contributors ?? [])
    .map((c) => c.author?.name)
    .filter(Boolean)
    .slice(0, 3) as string[];
  return authors.join(', ');
}

export function formatBookLine(book: Book): string {
  const author = authorLabel(book);
  const year = book.release_year ? ` (${book.release_year})` : '';
  return author ? `${book.title}${year} — ${author}` : `${book.title}${year}`;
}

export async function getWantToRead(limit = 20): Promise<UserBook[]> {
  const data = await graphql<{ me: Array<{ user_books: UserBook[] }> }>(
    `query WantToRead($limit: Int!) {
      me {
        user_books(where:{status_id:{_eq:${STATUS.WANT_TO_READ}}}, order_by:{date_added:desc}, limit:$limit) {
          id
          date_added
          book {
            id
            title
            release_year
            cached_contributors
          }
        }
      }
    }`,
    { limit },
  );
  return data.me[0]?.user_books ?? [];
}

export async function getShelf(statusId: number, limit = 100): Promise<UserBook[]> {
  const data = await graphql<{ me: Array<{ user_books: UserBook[] }> }>(
    `query Shelf($limit: Int!) {
      me {
        user_books(where:{status_id:{_eq:${statusId}}}, order_by:{date_added:desc}, limit:$limit) {
          id
          status_id
          date_added
          first_started_reading_date
          last_read_date
          user_book_status { status }
          book {
            id
            title
            release_year
            cached_contributors
          }
        }
      }
    }`,
    { limit },
  );
  return data.me[0]?.user_books ?? [];
}

export async function findExistingUserBooks(bookId: number): Promise<UserBook[]> {
  const data = await graphql<{ me: Array<{ user_books: UserBook[] }> }>(
    `query Existing($bookId: Int!) {
      me {
        user_books(where:{book_id:{_eq:$bookId}}, order_by:{date_added:desc}) {
          id
          status_id
          date_added
          first_started_reading_date
          last_read_date
          user_book_status { status }
          book {
            id
            title
            release_year
            cached_contributors
          }
        }
      }
    }`,
    { bookId },
  );
  return data.me[0]?.user_books ?? [];
}

export async function resolveBook(input: string): Promise<{ kind: 'exact'; book: Book } | { kind: 'ambiguous'; matches: Book[] } | { kind: 'none' }> {
  const normalized = normalizeTitle(input);

  const current = await getShelf(STATUS.CURRENTLY_READING, 100);
  const currentMatches = current.filter((ub) => normalizeTitle(ub.book.title) === normalized).map((ub) => ub.book);
  if (currentMatches.length === 1) return { kind: 'exact', book: currentMatches[0] };
  if (currentMatches.length > 1) return { kind: 'ambiguous', matches: currentMatches };

  const data = await graphql<{ search: { results: { hits?: SearchHit[] } } }>(
    `query Search($query: String!) {
      search(query:$query, query_type:"Book") {
        results
      }
    }`,
    { query: input },
  );

  const hits = data.search?.results?.hits ?? [];
  const books: Book[] = hits.map((hit) => ({
    id: Number(hit.document.id),
    title: hit.document.title,
    release_year: hit.document.release_year,
    cached_contributors: (hit.document.author_names ?? []).map((name) => ({ author: { name } })),
  }));

  const exact = books.filter((book) => normalizeTitle(book.title) === normalized);
  if (exact.length === 1) return { kind: 'exact', book: exact[0] };
  if (exact.length > 1) return { kind: 'ambiguous', matches: exact.slice(0, 5) };
  if (books.length === 1) return { kind: 'exact', book: books[0] };
  if (books.length > 1) return { kind: 'ambiguous', matches: books.slice(0, 5) };
  return { kind: 'none' };
}

export async function startReading(book: Book, startedAt = today()): Promise<UserBook> {
  const existing = await findExistingUserBooks(book.id);
  const current = existing.find((ub) => ub.status_id === STATUS.CURRENTLY_READING);
  if (current) return current;

  const prior = existing[0];
  if (prior) {
    const data = await graphql<{ update_user_book: { user_book: UserBook } }>(
      `mutation StartExisting($id: Int!, $object: UserBookUpdateInput!) {
        update_user_book(id:$id, object:$object) {
          user_book {
            id
            status_id
            first_started_reading_date
            last_read_date
            user_book_status { status }
            book { id title release_year cached_contributors }
          }
        }
      }`,
      { id: prior.id, object: { status_id: STATUS.CURRENTLY_READING, first_started_reading_date: startedAt } },
    );
    return data.update_user_book.user_book;
  }

  const data = await graphql<{ insert_user_book: { user_book: UserBook } }>(
    `mutation StartNew($object: UserBookCreateInput!) {
      insert_user_book(object:$object) {
        user_book {
          id
          status_id
          date_added
          first_started_reading_date
          last_read_date
          user_book_status { status }
          book { id title release_year cached_contributors }
        }
      }
    }`,
    { object: { book_id: book.id, status_id: STATUS.CURRENTLY_READING, first_started_reading_date: startedAt, date_added: startedAt } },
  );
  return data.insert_user_book.user_book;
}

export async function finishReading(book: Book, finishedAt = today()): Promise<UserBook> {
  const existing = await findExistingUserBooks(book.id);
  const current = existing.find((ub) => ub.status_id === STATUS.CURRENTLY_READING) ?? existing[0];
  if (!current) {
    throw new Error('No existing user_book entry found for this title. Start it first or add support for direct finished insertion.');
  }
  const data = await graphql<{ update_user_book: { user_book: UserBook } }>(
    `mutation Finish($id: Int!, $object: UserBookUpdateInput!) {
      update_user_book(id:$id, object:$object) {
        user_book {
          id
          status_id
          first_started_reading_date
          last_read_date
          user_book_status { status }
          book { id title release_year cached_contributors }
        }
      }
    }`,
    { id: current.id, object: { status_id: STATUS.READ, last_read_date: finishedAt } },
  );
  return data.update_user_book.user_book;
}

export async function countReadLastYear(): Promise<{ year: number; count: number; sample: UserBook[] }> {
  const now = new Date();
  const year = now.getUTCFullYear() - 1;
  const from = `${year}-01-01`;
  const to = `${year}-12-31`;
  const data = await graphql<{ me: Array<{ user_books: UserBook[]; user_books_aggregate: { aggregate: { count: number } } }> }>(
    `query CountLastYear($from: date!, $to: date!) {
      me {
        user_books(where:{status_id:{_eq:${STATUS.READ}}, last_read_date:{_gte:$from, _lte:$to}}, order_by:{last_read_date:desc}, limit:10) {
          id
          last_read_date
          book { id title release_year cached_contributors }
        }
        user_books_aggregate(where:{status_id:{_eq:${STATUS.READ}}, last_read_date:{_gte:$from, _lte:$to}}) {
          aggregate { count }
        }
      }
    }`,
    { from, to },
  );
  return {
    year,
    count: data.me[0]?.user_books_aggregate.aggregate.count ?? 0,
    sample: data.me[0]?.user_books ?? [],
  };
}

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

export function formatUserBookLine(userBook: UserBook): string {
  return formatBookLine(userBook.book);
}
