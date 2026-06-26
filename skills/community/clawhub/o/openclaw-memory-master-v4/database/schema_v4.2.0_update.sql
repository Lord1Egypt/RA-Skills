-- Memory-Master v4.2.0 Schema 更新
-- 添加迭代压缩和 Lineage 追踪支持
-- 日期：2026-04-11

-- ============ 1. 添加迭代压缩字段 ============

-- 父记忆 ID (用于 lineage 追踪)
ALTER TABLE memories ADD COLUMN parent_memory_id TEXT;

-- 压缩链 (JSON 数组，存储所有祖先 ID)
ALTER TABLE memories ADD COLUMN compression_chain TEXT;

-- 上次压缩摘要 (用于迭代压缩)
ALTER TABLE memories ADD COLUMN last_compressed_summary TEXT;

-- 是否是迭代压缩
ALTER TABLE memories ADD COLUMN is_iterative_compression INTEGER DEFAULT 0;

-- 压缩模板类型
ALTER TABLE memories ADD COLUMN compression_template TEXT DEFAULT 'standard';

-- ============ 2. 创建索引 ============

-- 父记忆索引 (加速 lineage 查询)
CREATE INDEX IF NOT EXISTS idx_memories_parent ON memories(parent_memory_id);

-- 压缩链索引 (加速谱系查询)
CREATE INDEX IF NOT EXISTS idx_memories_compression_chain ON memories(compression_chain);

-- 组合索引 (加速迭代压缩查询)
CREATE INDEX IF NOT EXISTS idx_memories_iterative 
ON memories(parent_memory_id, last_compressed_summary) 
WHERE last_compressed_summary IS NOT NULL;

-- ============ 3. 创建 Lineage 视图 ============

-- 记忆谱系视图 (递归查询)
CREATE VIEW IF NOT EXISTS memory_lineage AS
WITH RECURSIVE lineage AS (
  -- 基础情况：当前记忆
  SELECT 
    id,
    parent_memory_id,
    compression_chain,
    content,
    summary,
    created_at,
    0 as depth,
    id as root_id
  FROM memories
  WHERE parent_memory_id IS NULL
  
  UNION ALL
  
  -- 递归情况：子记忆
  SELECT 
    m.id,
    m.parent_memory_id,
    m.compression_chain,
    m.content,
    m.summary,
    m.created_at,
    l.depth + 1,
    l.root_id
  FROM memories m
  INNER JOIN lineage l ON m.parent_memory_id = l.id
)
SELECT * FROM lineage;

-- ============ 4. 创建压缩历史视图 ============

-- 压缩历史视图
CREATE VIEW IF NOT EXISTS compression_history AS
SELECT 
  m.id,
  m.parent_memory_id,
  m.compression_chain,
  m.summary,
  m.last_compressed_summary,
  m.is_iterative_compression,
  m.compression_template,
  m.created_at,
  m.compressed_at,
  -- 计算压缩率
  CASE 
    WHEN m.original_length > 0 
    THEN LENGTH(m.summary) * 1.0 / m.original_length
    ELSE NULL
  END as compression_ratio,
  -- 谱系深度
  (
    SELECT COUNT(*) FROM memories m2 
    WHERE m2.id IN (
      WITH RECURSIVE ancestors AS (
        SELECT parent_memory_id FROM memories WHERE id = m.id
        UNION ALL
        SELECT m3.parent_memory_id FROM memories m3
        INNER JOIN ancestors a ON m3.id = a.parent_memory_id
      )
      SELECT parent_memory_id FROM ancestors WHERE parent_memory_id IS NOT NULL
    )
  ) as lineage_depth
FROM memories m
WHERE m.summary IS NOT NULL;

-- ============ 5. 添加触发器 ============

-- 自动更新 compression_chain 的触发器
CREATE TRIGGER IF NOT EXISTS update_compression_chain
AFTER INSERT ON memories
WHEN NEW.parent_memory_id IS NOT NULL
BEGIN
  UPDATE memories
  SET compression_chain = (
    SELECT COALESCE(compression_chain, '[]')
    FROM memories
    WHERE id = NEW.parent_memory_id
  ) || ',"' || NEW.parent_memory_id || '"]'
  WHERE id = NEW.id;
END;

-- ============ 6. 添加示例数据 (测试用) ============

-- 插入测试记忆
INSERT INTO memories (
  id,
  type,
  content,
  summary,
  parent_memory_id,
  compression_chain,
  last_compressed_summary,
  is_iterative_compression,
  compression_template,
  created_at,
  compressed_at
) VALUES 
(
  'mem_test_1',
  'semantic',
  '这是原始内容，包含很多详细信息...',
  '核心要点 1\n核心要点 2',
  NULL,
  '[]',
  NULL,
  0,
  'standard',
  datetime('now'),
  datetime('now')
),
(
  'mem_test_2',
  'semantic',
  '这是新增的内容...',
  '核心要点 1\n核心要点 2\n新增要点 3',
  'mem_test_1',
  '["mem_test_1"]',
  '核心要点 1\n核心要点 2',
  1,
  'iterative',
  datetime('now'),
  datetime('now')
);

-- ============ 7. 查询示例 ============

-- 查询记忆的完整谱系
-- SELECT * FROM memory_lineage WHERE root_id = 'mem_test_2';

-- 查询压缩历史
-- SELECT * FROM compression_history WHERE id = 'mem_test_2';

-- 查询所有迭代压缩的记忆
-- SELECT * FROM memories WHERE is_iterative_compression = 1;

-- 查询谱系深度大于 2 的记忆
-- SELECT * FROM compression_history WHERE lineage_depth > 2;

-- ============ 更新说明 ============

-- v4.2.0 更新内容:
-- 1. 添加 parent_memory_id 支持 lineage 追踪
-- 2. 添加 compression_chain 存储完整谱系
-- 3. 添加 last_compressed_summary 支持迭代压缩
-- 4. 添加 is_iterative_compression 标记压缩类型
-- 5. 添加 compression_template 记录使用的模板
-- 6. 创建 memory_lineage 视图用于谱系查询
-- 7. 创建 compression_history 视图用于历史分析
-- 8. 添加触发器自动维护 compression_chain

-- 升级方法:
-- sqlite3 memory.db < schema_v4.2.0_update.sql
