import { X, ShoppingBag, Trash2, ArrowRight } from 'lucide-react';
import { useCartStore } from '../store/cartStore';
import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';

export default function CartDrawer() {
  const { items, isOpen, toggleCart, removeItem, updateQuantity, total } = useCartStore();
  const navigate = useNavigate();

  const handleCheckout = () => {
    toggleCart();
    navigate('/checkout');
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className={clsx(
          'fixed inset-0 z-50 bg-black/40 backdrop-blur-sm transition-opacity duration-300',
          isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        )}
        onClick={toggleCart}
      />

      {/* Drawer */}
      <div
        className={clsx(
          'fixed top-0 right-0 z-50 h-full w-full max-w-sm bg-white shadow-2xl flex flex-col transition-transform duration-300',
          isOpen ? 'translate-x-0' : 'translate-x-full'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-neutral-100">
          <div className="flex items-center gap-2">
            <ShoppingBag size={18} />
            <h2 className="font-display text-lg">Shopping Bag</h2>
            {items.length > 0 && (
              <span className="text-xs text-neutral-400">({items.length} item{items.length !== 1 ? 's' : ''})</span>
            )}
          </div>
          <button onClick={toggleCart} className="p-1 hover:opacity-60 transition-opacity" aria-label="Close cart">
            <X size={20} />
          </button>
        </div>

        {/* Items */}
        <div className="flex-1 overflow-y-auto">
          {items.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full gap-4 text-neutral-400">
              <ShoppingBag size={48} strokeWidth={1} />
              <p className="text-sm">Your shopping bag is empty</p>
              <button
                className="text-sm underline text-neutral-600 hover:text-neutral-900"
                onClick={() => {
                  toggleCart();
                  navigate('/shop');
                }}
              >
                Start shopping
              </button>
            </div>
          ) : (
            <ul className="divide-y divide-neutral-50">
              {items.map((item, idx) => (
                <li key={idx} className="flex gap-4 p-5">
                  <img
                    src={item.product.images[0]}
                    alt={item.product.name}
                    className="w-20 h-28 object-cover bg-neutral-100"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-neutral-400 uppercase tracking-wider">{item.product.brand}</p>
                    <p className="text-sm font-medium text-neutral-800 mt-0.5 truncate">{item.product.name}</p>
                    <p className="text-xs text-neutral-400 mt-0.5">
                      {item.selectedSize} &middot; {item.selectedColor}
                    </p>
                    <div className="flex items-center justify-between mt-3">
                      {/* Qty */}
                      <div className="flex items-center border border-neutral-200">
                        <button
                          className="w-7 h-7 flex items-center justify-center text-neutral-600 hover:bg-neutral-50 transition-colors text-lg leading-none"
                          onClick={() =>
                            updateQuantity(item.product.id, item.selectedSize, item.selectedColor, item.quantity - 1)
                          }
                          aria-label="Decrease quantity"
                        >
                          &minus;
                        </button>
                        <span className="w-8 text-center text-sm">{item.quantity}</span>
                        <button
                          className="w-7 h-7 flex items-center justify-center text-neutral-600 hover:bg-neutral-50 transition-colors text-lg leading-none"
                          onClick={() =>
                            updateQuantity(item.product.id, item.selectedSize, item.selectedColor, item.quantity + 1)
                          }
                          aria-label="Increase quantity"
                        >
                          +
                        </button>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold">
                          ${(item.product.price * item.quantity).toLocaleString()}
                        </span>
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
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Footer */}
        {items.length > 0 && (
          <div className="border-t border-neutral-100 p-6 space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-neutral-600">Subtotal</span>
              <span className="font-semibold">${total().toLocaleString()}</span>
            </div>
            <p className="text-xs text-neutral-400">Taxes and shipping calculated at checkout</p>
            <button className="btn-primary w-full gap-2" onClick={handleCheckout}>
              Checkout
              <ArrowRight size={16} />
            </button>
            <button
              className="btn-outline w-full text-xs"
              onClick={() => {
                toggleCart();
                navigate('/shop');
              }}
            >
              Continue Shopping
            </button>
          </div>
        )}
      </div>
    </>
  );
}
