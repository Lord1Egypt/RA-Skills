import { AlertTriangle, Check, Package, ShoppingBag, Truck, X } from 'lucide-react';
import { products } from '../data/products';
import { formatPrice } from '../utils/format';
import clsx from 'clsx';

// Mock orders — replace with a real query when the backend is wired.
const MOCK_ORDERS = [
  { id: 'SL1A2B3', customer: 'E. Moreau', total: 1980, status: 'shipped', items: 1, date: '2026-09-12' },
  { id: 'SL4C5D6', customer: 'J. Whitaker', total: 2640, status: 'processing', items: 2, date: '2026-09-11' },
  { id: 'SL7E8F9', customer: 'L. Novak', total: 680, status: 'delivered', items: 1, date: '2026-09-10' },
  { id: 'SL0G1H2', customer: 'M. Okafor', total: 3280, status: 'processing', items: 1, date: '2026-09-09' },
  { id: 'SL3I4J5', customer: 'S. Lindqvist', total: 2480, status: 'shipped', items: 2, date: '2026-09-08' },
];

const statusConfig = {
  processing: { icon: ShoppingBag, color: 'text-amber-600', bg: 'bg-amber-50', label: 'Processing' },
  shipped: { icon: Truck, color: 'text-blue-600', bg: 'bg-blue-50', label: 'Shipped' },
  delivered: { icon: Check, color: 'text-fresh-600', bg: 'bg-fresh-50', label: 'Delivered' },
  cancelled: { icon: X, color: 'text-red-600', bg: 'bg-red-50', label: 'Cancelled' },
};

const METRICS = [
  { label: 'Revenue', value: '¥124,800', change: '+12%', up: true },
  { label: 'Orders', value: '184', change: '+8%', up: true },
  { label: 'Conversion', value: '4.8%', change: '-0.3%', up: false },
  { label: 'Avg. order', value: '¥678', change: '+5%', up: true },
];

function AdminPage() {
  const topProducts = [...products].sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 4);

  return (
    <div className="mx-auto min-h-screen max-w-screen-xl px-4 py-10 pt-24 sm:px-6">
      <h1 className="mb-2 font-display text-3xl font-bold md:text-4xl">Admin</h1>
      <p className="mb-10 text-neutral-500">__BRAND_NAME__ store overview</p>

      {/* Metrics */}
      <div className="mb-12 grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6">
        {METRICS.map((m) => (
          <div key={m.label} className="rounded-2xl border border-neutral-200 bg-white p-5 md:p-6">
            <p className="mb-2 text-xs uppercase tracking-widest text-neutral-500">{m.label}</p>
            <p className="text-2xl font-bold text-neutral-900 md:text-3xl">{m.value}</p>
            <span className={clsx('text-xs font-medium', m.up ? 'text-fresh-600' : 'text-red-500')}>
              {m.change}
            </span>
          </div>
        ))}
      </div>

      <div className="grid gap-8 md:grid-cols-3">
        {/* Recent orders */}
        <div className="overflow-hidden rounded-2xl border border-neutral-200 bg-white md:col-span-2">
          <div className="flex items-center justify-between border-b border-neutral-100 px-6 py-4">
            <h2 className="font-display text-lg font-semibold">Recent orders</h2>
            <button className="text-xs text-neutral-500 transition-colors hover:text-brand-600">View all</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-neutral-100 text-left text-xs uppercase tracking-widest text-neutral-500">
                  <th className="px-6 py-3 font-medium">Order</th>
                  <th className="px-6 py-3 font-medium">Customer</th>
                  <th className="px-6 py-3 font-medium">Items</th>
                  <th className="px-6 py-3 text-right font-medium">Amount</th>
                  <th className="px-6 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {MOCK_ORDERS.map((o) => {
                  const cfg = statusConfig[o.status as keyof typeof statusConfig];
                  const Icon = cfg.icon;
                  return (
                    <tr key={o.id} className="border-b border-neutral-50 transition-colors hover:bg-neutral-50/50">
                      <td className="px-6 py-4">
                        <span className="font-medium text-neutral-900">{o.id}</span>
                        <p className="text-xs text-neutral-400">{o.date}</p>
                      </td>
                      <td className="px-6 py-4 text-neutral-700">{o.customer}</td>
                      <td className="px-6 py-4 text-neutral-600">{o.items}</td>
                      <td className="px-6 py-4 text-right font-medium text-neutral-900">
                        {formatPrice(o.total)}
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={clsx(
                            'inline-flex items-center gap-1 rounded-full px-2 py-1 text-[12px] font-medium',
                            cfg.bg,
                            cfg.color
                          )}
                        >
                          <Icon size={12} />
                          {cfg.label}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        <div className="space-y-8">
          {/* Top products */}
          <div className="overflow-hidden rounded-2xl border border-neutral-200 bg-white">
            <div className="border-b border-neutral-100 px-6 py-4">
              <h2 className="font-display text-lg font-semibold">Top products</h2>
            </div>
            <div className="divide-y divide-neutral-50">
              {topProducts.map((p, i) => (
                <div key={p.id} className="flex items-center gap-3 px-6 py-3">
                  <span className="flex h-5 w-5 items-center justify-center text-xs font-medium text-neutral-400">
                    {i + 1}
                  </span>
                  <img src={p.images[0]} alt={p.name} className="h-11 w-8 rounded bg-neutral-100 object-cover" />
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-xs font-medium text-neutral-800">{p.name}</p>
                    <p className="text-[12px] text-neutral-400">{p.reviewCount} reviews</p>
                  </div>
                  <span className="text-xs font-semibold text-neutral-900">{formatPrice(p.price)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Stock */}
          <div className="overflow-hidden rounded-2xl border border-neutral-200 bg-white">
            <div className="border-b border-neutral-100 px-6 py-4">
              <h2 className="font-display text-lg font-semibold">Stock levels</h2>
            </div>
            <div className="space-y-3 p-6">
              {products.map((p) => (
                <div key={p.id} className="flex items-center justify-between gap-3 text-sm">
                  <span className="truncate text-neutral-700">{p.name}</span>
                  {p.stock <= 10 ? (
                    <span className="flex shrink-0 items-center gap-1 text-[12px] font-medium text-amber-600">
                      <AlertTriangle size={12} />
                      Only {p.stock}
                    </span>
                  ) : (
                    <span className="flex shrink-0 items-center gap-1 text-[12px] font-medium text-fresh-600">
                      <Package size={12} />
                      {p.stock} in stock
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminPage;
