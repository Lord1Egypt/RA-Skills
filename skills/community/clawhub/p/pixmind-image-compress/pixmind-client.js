const API_KEY = process.env.PIXMIND_API_KEY;
const API_BASE = (process.env.PIXMIND_API_BASE || 'https://aihub-admin.aimix.pro').replace(/\/+$/, '');

export async function compressImage(body) {
  if (!API_KEY) {
    throw new Error('PIXMIND_API_KEY not set. Create one at https://www.pixmind.io/api-platform/dashboard/keys');
  }

  const res = await fetch(`${API_BASE}/api-platform/v1/image/compress`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`,
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (data.code !== 1000) {
    throw new Error(`API Error: ${data.message || JSON.stringify(data)}`);
  }
  return data.data;
}
