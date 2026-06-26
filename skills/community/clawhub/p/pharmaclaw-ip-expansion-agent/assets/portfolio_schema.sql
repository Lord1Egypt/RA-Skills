-- Run in agent._init_db()
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY,
    patent_num TEXT UNIQUE,
    title TEXT,
    filing_date DATE,
    expiration_date DATE,
    claims JSON,
    smiles TEXT,
    therapeutic TEXT,
    status TEXT
);
