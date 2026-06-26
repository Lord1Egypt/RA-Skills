// Starter pre-request script
// Replace placeholders with environment-specific logic.

if (!pm.environment.get("trace_id")) {
  pm.environment.set("trace_id", `trace-${Date.now()}`);
}

const token = pm.environment.get("access_token");
if (token) {
  pm.request.headers.upsert({ key: "Authorization", value: `Bearer ${token}` });
}

pm.request.headers.upsert({ key: "X-Trace-Id", value: pm.environment.get("trace_id") });
