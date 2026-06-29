"use client";

import { useState } from "react";

// Intentionally flawed fixture: a Client Component page.
// The scanner should flag `client-route-no-metadata` (ERROR) here —
// the metadata export below is silently dropped by Next.js.
export const metadata = { title: "Dashboard" };

export default function DashboardPage() {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setOpen(!open)}>Toggle</button>
      {open && <img src="/avatar.png" alt="avatar" />}
    </div>
  );
}
