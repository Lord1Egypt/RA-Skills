/**
 * 魔方网表列表组件 - React 示例
 *
 * 使用方式：
 * 1. 将 YOUR_SPACE_ID、YOUR_FORM_ID 替换为实际值
 * 2. 按需修改 DISPLAY_COLUMNS（字段 name 与 label 映射）
 * 3. 本地 mock 时设置 apiBase，同域部署时 apiBase 设为 ''
 *
 * 注意：API 返回的 key 是 name（英文），不能用 label（中文）作为 data 的 key
 */

import React, { useState, useEffect } from 'react';

// ========== 配置区 ==========
const CONFIG = {
  apiBase: '',
  spaceId: 'YOUR_SPACE_ID',
  formId: 'YOUR_FORM_ID',
  pageSize: 10,
};

// 展示列：name 为 API 字段标识，label 为表头显示
const DISPLAY_COLUMNS = [
  { name: 'id', label: '序号' },
  { name: 'mingcheng', label: '名称' },
  { name: 'jine', label: '金额' },
];

// ========== 步骤 1: 构建 API 路径 ==========
function getRecordsUrl(apiBase: string, spaceId: string, formId: string, start: number, limit: number): string {
  const path = `/magicflu/service/s/jsonv2/${spaceId}/forms/${formId}/records/entry`;
  const params = new URLSearchParams({ start: String(start), limit: String(limit) });
  const origin = apiBase ? apiBase.replace(/\/$/, '') : '';
  return `${origin}${path}?${params}`;
}

// ========== 步骤 2: 获取记录 ==========
async function fetchRecords(
  spaceId: string,
  formId: string,
  apiBase: string,
  page: number,
  pageSize: number
): Promise<{ entry: Record<string, unknown>[]; totalCount: number }> {
  const start = page * pageSize;
  const url = getRecordsUrl(apiBase, spaceId, formId, start, pageSize);

  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();

  if (!data.entry) throw new Error('响应格式异常');
  return { entry: data.entry, totalCount: data.totalCount ?? 0 };
}

// ========== 组件 ==========
function MagicfluList() {
  const [data, setData] = useState<Record<string, unknown>[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { apiBase, spaceId, formId, pageSize } = CONFIG;

  // 步骤 3: 加载数据
  useEffect(() => {
    setLoading(true);
    setError(null);

    fetchRecords(spaceId, formId, apiBase, page, pageSize)
      .then(({ entry, totalCount }) => {
        setData(entry);
        setTotalCount(totalCount);
      })
      .catch((e) => {
        setError(
          e.message?.includes('加载失败')
            ? e.message
            : '加载失败，请检查网络或空间/表单 ID 是否正确。'
        );
      })
      .finally(() => setLoading(false));
  }, [apiBase, spaceId, formId, page, pageSize]);

  const totalPages = Math.ceil(totalCount / pageSize) || 1;

  // 步骤 4: 渲染单元格值（dropdown 等可能返回 { value, content }）
  const getCellValue = (row: Record<string, unknown>, name: string): unknown => {
    const val = row[name];
    if (val && typeof val === 'object' && 'content' in val) {
      return (val as { content: unknown }).content;
    }
    return val;
  };

  if (loading) return <div>加载中...</div>;
  if (error) return <div style={{ color: '#c00' }}>{error}</div>;

  return (
    <div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {DISPLAY_COLUMNS.map((c) => (
              <th key={c.name} style={{ border: '1px solid #ddd', padding: 10, textAlign: 'left' }}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={(row.id as string) ?? i}>
              {DISPLAY_COLUMNS.map((c) => (
                <td key={c.name} style={{ border: '1px solid #ddd', padding: 10 }}>
                  {String(getCellValue(row, c.name) ?? '-')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: 16, display: 'flex', gap: 8, alignItems: 'center' }}>
        <button
          disabled={page <= 0}
          onClick={() => setPage((p) => p - 1)}
        >
          上一页
        </button>
        <span>
          第 {page + 1} / {totalPages} 页，共 {totalCount} 条
        </span>
        <button
          disabled={page >= totalPages - 1}
          onClick={() => setPage((p) => p + 1)}
        >
          下一页
        </button>
      </div>
    </div>
  );
}

export default MagicfluList;
