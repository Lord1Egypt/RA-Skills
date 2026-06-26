import { products } from '../data/products';
import { Check, AlertTriangle, ShoppingBag, TrendingUp } from 'lucide-react';
import clsx from 'clsx';

// Mock orders
const MOCK_ORDERS = [
  { id: 'SL1A2B3', customer: 'Alice W.', total: 1280, status: 'shipped', items: 1, date: '2025-01-12' },
  { id: 'SL4C5D6', customer: 'Bob T.', total: 2640, status: 'processing', items: 2, date: '2025-01-11' },
  { id: 'SL7E8F9', customer: 'Carol L.', total: 680, status: 'delivered', items: 1, date: '2025-01-10' },
  { id: 'SL0G1H2', customer: 'David K.', total: 1980, status: 'processing', items: 1, date: '2025-01-09' },
  { id: 'SL3I4J5', customer: 'Eva M.', total: 2480, status: 'shipped', items: 2, date: '2025-01-08' },
];

const statusConfig = {
  processing: { icon: ShoppingBag, color: 'text-amber-600', bg: 'bg-amber-50', label: 'Processing' },
  shipped: { icon: Truck, color: 'text-blue-600', bg: 'bg-blue-50', label: 'Shipped' },
  delivered: { icon: Check, color: 'text-green-600', bg: 'bg-green-50', label: 'Delivered' },
  cancelled: { icon: X, color: 'text-red-600', bg: 'bg-red-50', label: 'Cancelled' },
};

function AdminPage() {
  const topProducts = [...products].sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 4);
  const lowStock = products.filter((p) => p.isNew === false); // mock: pretend non-new items are low stock

  return (
    <div className="min-h-screen pt-24 max-w-screen-xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="font-display text-3xl md:text-4xl font-bold mb-2">Admin Dashboard</h1>
      <p className="text-neutral-500 mb-10">Manage __BRAND_NAME__ store</p>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mb-12">
        {[
          { label: 'Revenue', value: '$12.4k', change: '+12%', up: true },
          { label: 'Orders', value: '184', change: '+8%', up: true },
          { label: 'Conversion', value: '4.8%', change: '-0.3%', up: false },
          { label: 'Avg Order', value: '$89', change: '+5%', up: true },
        ].map((m) => (
          <div key={m.label} className="bg-white border border-neutral-200 p-5 md:p-6">
            <p className="text-xs text-neutral-500 tracking-widest uppercase mb-2">{m.label}</p>
            <p className="text-2xl md:text-3xl font-bold text-neutral-900">{m.value}</p>
            <span className={clsx('text-xs font-medium', m.up ? 'text-green-600' : 'text-red-500')}>
              {m.change}
            </span>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Recent Orders */}
        <div className="md:col-span-2 bg-white border border-neutral-200">
          <div className="flex items-center justify-between px-6 py-4 border-b border-neutral-100">
            <h2 className="font-display text-lg font-semibold">Recent Orders</h2>
            <button className="text-xs text-neutral-500 hover:text-neutral-900 transition-colors">View All</button>
          </div>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-neutral-100 text-left text-xs text-neutral-500 tracking-widest uppercase">
                <th className="px-6 py-3 font-medium">Order</th>
                <th className="px-6 py-3 font-medium">Customer</th>
                <th className="px-6 py-3 font-medium">Items</th>
                <th className="px-6 py-3 font-medium text-right">Total</th>
                <th className="px-6 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {MOCK_ORDERS.map((o) => {
                const cfg = statusConfig[o.status as keyof typeof statusConfig];
                const Icon = cfg?.icon || ShoppingBag;
                return (
                  <tr key={o.id} className="border-b border-neutral-50 hover:bg-neutral-50/50 transition-colors">
                    <td className="px-6 py-4">
                      <span className="font-medium text-neutral-900">{o.id}</span>
                      <p className="text-xs text-neutral-400">{o.date}</p>
                    </td>
                    <td className="px-6 py-4 text-neutral-700">{o.customer}</td>
                    <td className="px-6 py-4 text-neutral-600">{o.items}</td>
                    <td className="px-6 py-4 text-right font-medium text-neutral-900">${o.total.toLocaleString()}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 ${cfg.bg} ${cfg.color} text-[10px] font-semibold uppercase tracking-wider rounded`}>
                        <Icon size={10} />
                        {cfg.label}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Right Column: Hot Products + Stock */}
        <div className="space-y-8">
          {/* Hot Products */}
          <div className="bg-white border border-neutral-200">
            <div className="px-6 py-4 border-b border-neutral-100">
              <h2 className="font-display text-lg font-semibold">Top Products</h2>
            </div>
            <div className="divide-y divide-neutral-50">
              {topProducts.map((p, i) => (
                <div key={p.id} className="flex items-center gap-3 px-6 py-3">
                  <span className="w-5 h-5 flex items-center justify-center text-xs text-neutral-400 font-medium">{i + 1}</span>
                  <img src={p.images[0]} alt={p.name} className="w-8 h-11 object-cover bg-neutral-100" />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-neutral-800 truncate">{p.name}</p>
                    <p className="text-[10px] text-neutral-400">{p.reviewCount} reviews</p>
                  </div>
                  <span className="text-xs font-semibold text-neutral-900">${p.price.toLocaleString()}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Stock Overview */}
          <div className="bg-white border border-neutral-200">
            <div className="px-6 py-4 border-b border-neutral-100">
              <h2 className="font-display text-lg font-semibold">Stock Overview</h2>
            </div>
            <div className="p-6 space-y-3">
              {products.map((p) => {
                const isLow = lowStock.includes(p);
                return (
                  <div key={p.id} className="flex items-center justify-between text-sm">
                    <span className="text-neutral-700 truncate">{p.name}</span>
                    {isLow ? (
                      <span className="flex items-center gap-1 text-[10px] text-amber-600 font-medium">
                        <AlertTriangle size={10} />
                        Restock
                      </span>
                    ) : (
                      <span className="text-[10px] text-green-600 font-medium">In Stock</span>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminPage;
