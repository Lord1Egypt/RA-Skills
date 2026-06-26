-- Table: vault_chunks
-- Stores chunked and embedded content from Obsidian vault notes
-- for RAG (Retrieval-Augmented Generation) search.

create table if not exists vault_chunks (
  id bigint primary key generated always as identity,
  file_path text not null,
  chunk_index integer not null,
  content text not null,
  embedding vector(384),
  metadata jsonb default '{}'::jsonb,
  updated_at timestamp with time zone default now(),
  unique (file_path, chunk_index)
);

create index if not exists idx_vault_chunks_file_path
  on vault_chunks (file_path);

create index if not exists idx_vault_chunks_embedding
  on vault_chunks using hnsw (embedding vector_cosine_ops);

-- RPC: match_vault_chunks
-- Cosine similarity search against vault_chunks embeddings.
-- Same pattern as match_markets.

create or replace function match_vault_chunks(
  query_embedding vector(384),
  match_threshold float default 0.65,
  match_count int default 5,
  filter_category text default null
)
returns table (
  id bigint,
  file_path text,
  chunk_index integer,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
    select
      vc.id,
      vc.file_path,
      vc.chunk_index,
      vc.content,
      vc.metadata,
      1 - (vc.embedding <=> query_embedding) as similarity
    from vault_chunks vc
    where 1 - (vc.embedding <=> query_embedding) > match_threshold
      and (filter_category is null or vc.metadata->>'category' = filter_category)
    order by vc.embedding <=> query_embedding
    limit match_count;
end;
$$;
