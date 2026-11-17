import { ArrowRight, Minus, Plus, ShoppingBag, Trash2, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import { FREE_SHIPPING_THRESHOLD, formatPrice } from '../utils/format';
import clsx from 'clsx';

export default function CartDrawer() {
  const { items, isOpen, toggleCart, removeItem, updateQuantity, total } = useCartStore();
  const navigate = useNavigate();

  const subtotal = total();

  const goTo = (path: string) => {
    toggleCart();
    navigate(path);
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className={clsx(
          'fixed inset-0 z-50 bg-black/40 backdrop-blur-sm transition-opacity duration-300',
          isOpen ? 'pointer-events-auto opacity-100' : 'pointer-events-none opacity-0'
        )}
        onClick={toggleCart}
      />

      {/* Drawer */}
      <div
        className={clsx(
          'fixed right-0 top-0 z-50 flex h-full w-full max-w-sm flex-col bg-white shadow-2xl transition-transform duration-300',
          isOpen ? 'translate-x-0' : 'translate-x-full'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b border-neutral-100 px-6 py-5">
          <div className="flex items-center gap-2">
            <ShoppingBag size={18} />
            <h2 className="font-display text-lg">Cart</h2>
            {items.length > 0 && (
              <span className="text-xs text-neutral-400">({items.length})</span>
            )}
          </div>
          <button onClick={toggleCart} className="p-1 transition-opacity hover:opacity-60" aria-label="Close cart">
            <X size={20} />
          </button>
        </div>

        {/* Items */}
        <div className="flex-1 overflow-y-auto">
          {items.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center gap-4 text-neutral-400">
              <ShoppingBag size={48} strokeWidth={1} />
              <p className="text-sm">Your cart is empty</p>
              <button className="text-sm text-brand-600 underline hover:text-brand-700" onClick={() => goTo('/shop')}>
                Start shopping
              </button>
            </div>
          ) : (
            <ul className="divide-y divide-neutral-50">
              {items.map((item, idx) => (
                <li key={`${item.product.id}-${item.selectedSize}-${item.selectedColor}-${idx}`} className="flex gap-4 p-5">
                  <img
                    src={item.product.images[0]}
                    alt={item.product.name}
                    className="h-28 w-20 rounded-lg bg-neutral-100 object-cover"
                  />
                  <div className="min-w-0 flex-1">
                    <p className="text-[12px] uppercase tracking-wider text-neutral-400">{item.product.brand}</p>
                    <p className="mt-0.5 truncate text-sm font-medium text-neutral-800">{item.product.name}</p>
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
                        <span className="text-sm font-semibold">{formatPrice(item.product.price * item.quantity)}</span>
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
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Footer */}
        {items.length > 0 && (
          <div className="space-y-4 border-t border-neutral-100 p-6">
            <div className="flex items-center justify-between">
              <span className="text-sm text-neutral-600">Subtotal</span>
              <span className="font-semibold">{formatPrice(subtotal)}</span>
            </div>
            <p className="text-xs text-neutral-400">
              {subtotal >= FREE_SHIPPING_THRESHOLD
                ? 'Free shipping unlocked — it is applied automatically at checkout'
                : `Add ${formatPrice(FREE_SHIPPING_THRESHOLD - subtotal)} more for free shipping`}
            </p>
            <button className="btn-primary w-full" onClick={() => goTo('/checkout')}>
              Checkout
              <ArrowRight size={16} />
            </button>
            <button className="btn-outline w-full" onClick={() => goTo('/shop')}>
              Continue shopping
            </button>
          </div>
        )}
      </div>
    </>
  );
}
