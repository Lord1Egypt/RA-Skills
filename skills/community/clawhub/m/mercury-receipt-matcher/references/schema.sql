PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY,
  source_file TEXT NOT NULL,
  source_row_number INTEGER NOT NULL,
  txn_date TEXT NOT NULL,
  merchant TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  currency TEXT DEFAULT 'USD',
  csv_status TEXT,
  source_account TEXT,
  bank_description TEXT,
  reference TEXT,
  note TEXT,
  last_four TEXT,
  cardholder_name TEXT,
  cardholder_email TEXT,
  merchant_type TEXT,
  category TEXT,
  gl_code TEXT,
  timestamp_utc TEXT,
  raw_csv_json TEXT,
  status TEXT NOT NULL DEFAULT 'pending',
  status_reason TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(source_file, source_row_number)
);

CREATE TABLE IF NOT EXISTS search_attempts (
  id INTEGER PRIMARY KEY,
  transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
  searched_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  source_type TEXT NOT NULL DEFAULT 'gmail_account',
  source_name TEXT NOT NULL,
  query TEXT NOT NULL,
  date_window_start TEXT,
  date_window_end TEXT,
  result_count INTEGER,
  outcome TEXT NOT NULL,
  error_detail TEXT
);

CREATE TABLE IF NOT EXISTS receipt_candidates (
  id INTEGER PRIMARY KEY,
  transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
  search_attempt_id INTEGER REFERENCES search_attempts(id) ON DELETE SET NULL,
  account TEXT NOT NULL,
  message_id TEXT NOT NULL,
  thread_id TEXT,
  from_address TEXT,
  subject TEXT,
  message_date TEXT,
  merchant_domain_ok INTEGER,
  amount_match INTEGER,
  matched_amount_cents INTEGER,
  disposition TEXT NOT NULL,
  reason TEXT,
  UNIQUE(account, message_id)
);

CREATE TABLE IF NOT EXISTS forwards (
  id INTEGER PRIMARY KEY,
  transaction_id INTEGER NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
  receipt_candidate_id INTEGER REFERENCES receipt_candidates(id) ON DELETE SET NULL,
  forwarded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  destination_email TEXT NOT NULL,
  account TEXT NOT NULL,
  source_message_id TEXT NOT NULL,
  status TEXT NOT NULL,
  provider_message_id TEXT,
  error_code TEXT,
  error_detail TEXT,
  UNIQUE(transaction_id, source_message_id, destination_email)
);
