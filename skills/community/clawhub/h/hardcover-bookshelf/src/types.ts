export type Contributor = {
  author?: {
    id?: number;
    name?: string;
  };
  contribution?: string | null;
};

export type Book = {
  id: number;
  title: string;
  slug?: string;
  release_year?: number | null;
  cached_contributors?: Contributor[];
};

export type UserBook = {
  id: number;
  status_id?: number | null;
  date_added?: string | null;
  first_started_reading_date?: string | null;
  last_read_date?: string | null;
  book: Book;
  user_book_status?: {
    status: string;
  } | null;
};

export type SearchHit = {
  document: {
    id: string | number;
    title: string;
    subtitle?: string;
    release_year?: number;
    author_names?: string[];
  };
};
