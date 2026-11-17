import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, Minus, Plus, ShoppingBag, Trash2 } from 'lucide-react';
import { useCartStore } from '../store/cartStore';
import { FREE_SHIPPING_THRESHOLD, formatPrice } from '../utils/format';

export default function CartPage() {
  const { items, removeItem, updateQuantity, total } = useCartStore();
  const navigate = useNavigate();

  const subtotal = total();

  return (
    <div className="min-h-screen pt-24">
      <div className="mx-auto max-w-screen-xl px-4 py-10 sm:px-6">
        <h1 className="mb-8 font-display text-3xl font-semibold md:text-4xl">Cart</h1>

        {items.length === 0 ? (
          <div className="py-32 text-center text-neutral-400">
            <ShoppingBag size={48} strokeWidth={1} className="mx-auto mb-4" />
            <p className="mb-2 text-lg">Your cart is empty</p>
            <p className="mb-6 text-sm">Add a few pieces you like.</p>
            <Link to="/shop" className="btn-primary">
              Start shopping
            </Link>
          </div>
        ) : (
          <div className="grid gap-10 md:grid-cols-3">
            {/* Items */}
            <div className="divide-y divide-neutral-100 md:col-span-2">
              {items.map((item, idx) => (
                <div
                  key={`${item.product.id}-${item.selectedSize}-${item.selectedColor}-${idx}`}
                  className="flex gap-4 py-6"
                >
                  <Link to={`/product/${item.product.id}`} className="shrink-0">
                    <img
                      src={item.product.images[0]}
                      alt={item.product.name}
                      className="h-32 w-24 rounded-lg bg-neutral-100 object-cover"
                    />
                  </Link>
                  <div className="min-w-0 flex-1">
                    <p className="text-[12px] uppercase tracking-wider text-neutral-400">{item.product.brand}</p>
                    <Link to={`/product/${item.product.id}`}>
                      <h3 className="mt-0.5 text-sm font-medium text-neutral-800 hover:text-brand-600">
                        {item.product.name}
                      </h3>
                    </Link>
                    <p className="mt-0.5 text-xs text-neutral-400">
                      {item.selectedSize} · {item.selectedColor}
                    </p>
                    <div className="mt-3 flex items-center justify-between">
                      <div className="flex items-center rounded-full border border-neutral-200">
                        <button
                          className="flex h-7 w-7 items-center justify-center text-neutral-600 transition-colors hover:bg-neutral-50"
                          onClick={() =>
                            updateQuantity(item.product.id, item.selectedSize, item.selectedColor, item.quantity - 1)
                          }
                          aria-label="Decrease quantity"
                        >
                          <Minus size={12} />
                        </button>
                        <span className="w-8 text-center text-sm">{item.quantity}</span>
                        <button
                          className="flex h-7 w-7 items-center justify-center text-neutral-600 transition-colors hover:bg-neutral-50"
                          onClick={() =>
                            updateQuantity(item.product.id, item.selectedSize, item.selectedColor, item.quantity + 1)
                          }
                          aria-label="Increase quantity"
                        >
                          <Plus size={12} />
                        </button>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold">
                          {formatPrice(item.product.price * item.quantity)}
                        </span>
                        <button
                          className="p-1 text-neutral-400 transition-colors hover:text-neutral-700"
                          onClick={() => removeItem(item.product.id, item.selectedSize, item.selectedColor)}
                          aria-label="Remove item"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className="h-fit md:sticky md:top-24">
              <div className="space-y-4 rounded-2xl border border-neutral-200 p-6">
                <h3 className="mb-2 text-lg font-semibold">Order summary</h3>
                <div className="flex justify-between text-sm">
                  <span className="text-neutral-600">Subtotal</span>
                  <span className="font-medium">{formatPrice(subtotal)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-neutral-600">Shipping</span>
                  <span className="text-neutral-500">
                    {subtotal >= FREE_SHIPPING_THRESHOLD ? 'Free' : 'Calculated at checkout'}
                  </span>
                </div>
                <div className="flex justify-between border-t border-neutral-200 pt-4 font-semibold">
                  <span>Total</span>
                  <span>{formatPrice(subtotal)}</span>
                </div>
                <button onClick={() => navigate('/checkout')} className="btn-primary mt-2 w-full">
                  Checkout
                  <ArrowRight size={16} />
                </button>
                <Link to="/shop" className="btn-outline w-full">
                  Continue shopping
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
