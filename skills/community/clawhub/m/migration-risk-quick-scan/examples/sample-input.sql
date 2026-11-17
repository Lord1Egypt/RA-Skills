-- Example input for migration-risk-quick-scan (free edition).
-- A realistic, dangerous migration: it renames a column the dangerous
-- way, tightens a column, and builds an index the blocking way.
ALTER TABLE users DROP COLUMN name;
ALTER TABLE users ADD COLUMN display_name TEXT;
ALTER TABLE users ADD COLUMN email TEXT NOT NULL;
CREATE INDEX idx_users_email ON users (email);
