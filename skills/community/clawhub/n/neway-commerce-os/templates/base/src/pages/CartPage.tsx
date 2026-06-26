import { Link } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';
import { Trash2, ArrowRight } from 'lucide-react';
import clsx from 'clsx';

export default function CartPage() {
  const { items, removeItem, updateQuantity, total, toggleCart } = useCartStore();
  const navigate = (path: string) => {
    toggleCart();
    window.location.href = path;
  };

  const handleCheckout = () => {
    toggleCart();
    window.location.href = '/checkout';
  };

  return (
    <div className="min-h-screen pt-24 max-w-screen-xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="font-display text-3xl md:text-4xl font-semibold mb-8">Shopping Bag</h1>

      {items.length === 0 ? (
        <div className="text-center py-32 text-neutral-400">
          <div className="mb-4">
            <svg width={48} height={48} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1} className="mx-auto">
              <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4zM3 6h18" />
              <path d="M16 10a4 4 0 11-8 0" />
            </svg>
          </div>
          <p className="text-lg mb-2">Your bag is empty</p>
          <Link to="/shop" className="btn-primary mt-4">
            Start Shopping
          </Link>
        </div>
      ) : (
        <div className="grid md:grid-cols-3 gap-10">
          {/* Items */}
          <div className="md:col-span-2 divide-y divide-neutral-100">
            {items.map((item, idx) => (
              <div key={`${item.product.id}-${item.selectedSize}-${item.selectedColor}-${idx}`} className="flex gap-4 py-6">
                <img
                  src={item.product.images[0]}
                  alt={item.product.name}
                  className="w-24 h-32 object-cover bg-neutral-100 shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-neutral-400 uppercase tracking-wider">{item.product.brand}</p>
                  <h3 className="text-sm font-medium text-neutral-800 mt-0.5">{item.product.name}</h3>
                  <p className="text-xs text-neutral-400 mt-0.5">
                    {item.selectedSize} &middot; {item.selectedColor}
                  </p>
                  <div className="flex items-center justify-between mt-3">
                    <div className="flex items-center border border-neutral-200">
                      <button
                        className="w-7 h-7 flex items-center justify-center text-neutral-600 hover:bg-neutral-50 transition-colors text-lg leading-none"
                        onClick={() => updateQuantity(item.product.id, item.selectedSize, item.selectedColor, item.quantity - 1)}
                        aria-label="Decrease quantity"
                      >
                        &minus;
                      </button>
                      <span className="w-8 text-center text-sm">{item.quantity}</span>
                      <button
                        className="w-7 h-7 flex items-center justify-center text-neutral-600 hover:bg-neutral-50 transition-colors text-lg leading-none"
                        onClick={() => updateQuantity(item.product.id, item.selectedSize, item.selectedColor, item.quantity + 1)}
                        aria-label="Increase quantity"
                      >
                        +
                      </button>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold">${(item.product.price * item.quantity).toLocaleString()}</span>
                      <button
                        className="p-1 text-neutral-400 hover:text-neutral-700 transition-colors"
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
          <div className="md:sticky md:top-24 h-fit">
            <div className="border border-neutral-200 p-6 space-y-4">
              <h3 className="font-semibold text-lg mb-2">Order Summary</h3>
              <div className="flex justify-between text-sm">
                <span className="text-neutral-600">Subtotal</span>
                <span className="font-medium">${total().toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-neutral-600">Shipping</span>
                <span className="text-neutral-500">Calculated at checkout</span>
              </div>
              <div className="border-t border-neutral-200 pt-4 flex justify-between font-semibold">
                <span>Estimated Total</span>
                <span>${total().toLocaleString()}</span>
              </div>
              <button onClick={handleCheckout} className="btn-primary w-full gap-2 mt-2">
                Proceed to Checkout
                <ArrowRight size={16} />
              </button>
              <button
                onClick={() => { toggleCart(); window.location.href = '/shop'; }}
                className="btn-outline w-full text-xs"
              >
                Continue Shopping
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
