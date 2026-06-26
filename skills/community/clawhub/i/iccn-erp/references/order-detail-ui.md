# 订单详情查询界面 - React 参考代码

以下是完整的 React Artifact 示例，可直接用于创建订单查询界面。

```jsx
import { useState } from "react";

export default function OrderQuery() {
  const [orderNo, setOrderNo] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleQuery = async () => {
    if (!orderNo.trim()) {
      setError("请输入订单编号");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(
        `https://dev.iccn.cc/api/openclaw/order_detail?order_no=${encodeURIComponent(orderNo.trim())}`
      );
      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.message || "查询失败，请检查订单号是否正确");
      }
    } catch (err) {
      setError("网络请求失败，请检查网络连接");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", padding: "0 20px", fontFamily: "sans-serif" }}>
      <h2 style={{ marginBottom: 24 }}>📦 订单详情查询</h2>

      {/* 输入区域 */}
      <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
        <input
          type="text"
          value={orderNo}
          onChange={(e) => setOrderNo(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleQuery()}
          placeholder="请输入订单编号，如 SO20240001"
          style={{
            flex: 1, padding: "10px 14px", border: "1px solid #d1d5db",
            borderRadius: 8, fontSize: 14, outline: "none"
          }}
        />
        <button
          onClick={handleQuery}
          disabled={loading}
          style={{
            padding: "10px 20px", background: loading ? "#9ca3af" : "#2563eb",
            color: "white", border: "none", borderRadius: 8,
            fontSize: 14, cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "查询中..." : "查询"}
        </button>
      </div>

      {/* 错误提示 */}
      {error && (
        <div style={{ padding: "12px 16px", background: "#fef2f2", border: "1px solid #fecaca", borderRadius: 8, color: "#dc2626", marginBottom: 16 }}>
          ❌ {error}
        </div>
      )}

      {/* 查询结果 */}
      {result && (
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden" }}>
          <div style={{ background: "#f9fafb", padding: "12px 16px", borderBottom: "1px solid #e5e7eb", fontWeight: 600 }}>
            订单信息
          </div>
          <div style={{ padding: 16 }}>
            {Object.entries(result).map(([key, value]) => (
              <div key={key} style={{ display: "flex", padding: "8px 0", borderBottom: "1px solid #f3f4f6" }}>
                <span style={{ width: 140, color: "#6b7280", fontSize: 13 }}>{key}</span>
                <span style={{ flex: 1, fontSize: 13 }}>{String(value)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```
