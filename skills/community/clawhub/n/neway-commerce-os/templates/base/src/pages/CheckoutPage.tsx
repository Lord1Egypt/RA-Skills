import { FormEvent, useEffect, useState } from 'react';
import { useCartStore } from '../store/cartStore';
import { useNavigate } from 'react-router-dom';
import { Check, ChevronLeft, ChevronRight, Truck, CreditCard, Shield, FileText } from 'lucide-react';
import { PROMO_CODES } from '../data/products';
import clsx from 'clsx';

const SHIPPING_METHODS = [
  { id: 'sf', name: 'Express Delivery', desc: 'SF Express · 1-2 days', fee: 15, freeAbove: 299 },
  { id: 'standard', name: 'Standard Shipping', desc: '3-5 business days', fee: 8, freeAbove: 299 },
  { id: 'economy', name: 'Economy Shipping', desc: '7-10 business days', fee: 0, freeAbove: 0 },
];

const PAYMENT_METHODS = [
  { id: 'wechat', name: 'WeChat Pay', icon: '💬' },
  { id: 'alipay', name: 'Alipay', icon: '🔵' },
  { id: 'bank', name: 'Bank Card', icon: '🏦' },
];

const PROVINCES = [
  'Beijing', 'Shanghai', 'Guangdong', 'Zhejiang', 'Jiangsu',
  'Sichuan', 'Hubei', 'Hunan', 'Fujian', 'Shaanxi',
];

function CheckoutPage() {
  const items = useCartStore((state) => state.items);
  const clearCart = useCartStore((state) => state.clearCart);
  const total = useCartStore((state) => state.total);
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [orderId, setOrderId] = useState('');

  // Step 1: Shipping
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [province, setProvince] = useState('');
  const [city, setCity] = useState('');
  const [district, setDistrict] = useState('');
  const [address, setAddress] = useState('');
  const [shippingMethod, setShippingMethod] = useState('sf');

  // Step 2: Payment & Promo
  const [promoCode, setPromoCode] = useState('');
  const [promoApplied, setPromoApplied] = useState<{ code: string; discount: number; type: 'percent' | 'fixed' } | null>(null);
  const [promoError, setPromoError] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('wechat');
  const [invoice, setInvoice] = useState(false);
  const [invoiceTitle, setInvoiceTitle] = useState('');
  const [notes, setNotes] = useState('');

  // Step 3: Review
  const [agreed, setAgreed] = useState(false);

  useEffect(() => {
    if (items.length === 0 && !orderId) {
      navigate('/cart');
    }
  }, [items, orderId, navigate]);

  const selectedShipping = SHIPPING_METHODS.find((m) => m.id === shippingMethod);
  const shippingFee = total() >= (selectedShipping?.freeAbove || 0) ? 0 : (selectedShipping?.fee || 0);
  const discount = promoApplied
    ? promoApplied.type === 'percent'
      ? Math.round(total() * promoApplied.discount / 100)
      : promoApplied.discount
    : 0;
  const grandTotal = total() + shippingFee - discount;

  const handleApplyPromo = () => {
    setPromoError('');
    const trimmed = promoCode.trim().toUpperCase();
    const found = Object.values(PROMO_CODES).find((c) => c.code === trimmed);
    if (found) {
      setPromoApplied({ code: found.code, discount: found.discount, type: found.type });
    } else {
      setPromoError('Invalid promo code');
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (step < 3) {
      setStep(step + 1);
      return;
    }
    // Final submit
    setSubmitting(true);
    await new Promise((r) => setTimeout(r, 1500));
    const id = 'SL' + Date.now().toString(36).toUpperCase();
    setOrderId(id);
    clearCart();
    setSubmitting(false);
  };

  const goBack = () => {
    if (step > 1) setStep(step - 1);
  };

  if (orderId) {
    return (
      <div className="min-h-screen pt-24 max-w-screen-xl mx-auto px-4 sm:px-6 py-16 text-center">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <Check size={28} className="text-green-600" />
        </div>
        <h1 className="font-display text-3xl font-bold mb-2">Order Confirmed!</h1>
        <p className="text-neutral-500 mb-1">Order #: {orderId}</p>
        <p className="text-sm text-neutral-400 mb-8">
          Thank you for your purchase. Estimated delivery: 1-3 business days.
        </p>
        <div className="flex items-center justify-center gap-4">
          <button onClick={() => navigate('/shop')} className="btn-primary">
            Continue Shopping
          </button>
          <button onClick={() => navigate('/')} className="btn-outline">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-24 max-w-screen-xl mx-auto px-4 sm:px-6 py-10">
      {/* Progress Stepper */}
      <div className="flex items-center justify-center gap-3 mb-12">
        {[
          { n: 1, label: 'Shipping' },
          { n: 2, label: 'Payment' },
          { n: 3, label: 'Review' },
        ].map((s) => (
          <div key={s.n} className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div
                className={clsx(
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-300',
                  step > s.n
                    ? 'bg-green-600 text-white'
                    : step === s.n
                    ? 'bg-neutral-900 text-white'
                    : 'bg-neutral-100 text-neutral-400'
                )}
              >
                {step > s.n ? <Check size={14} /> : s.n}
              </div>
              <span
                className={clsx(
                  'text-sm font-medium hidden sm:inline',
                  step >= s.n ? 'text-neutral-900' : 'text-neutral-400'
                )}
              >
                {s.label}
              </span>
            </div>
            {s.n < 3 && (
              <div className={clsx('w-8 h-0.5 transition-all duration-300', step > s.n ? 'bg-green-600' : 'bg-neutral-200')} />
            )}
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {/* Main Form */}
        <form onSubmit={handleSubmit} className="md:col-span-2 space-y-6">
          {/* Step 1: Shipping */}
          {step === 1 && (
            <div className="border border-neutral-200 p-6">
              <h2 className="font-display text-lg font-semibold mb-6 flex items-center gap-2">
                <Truck size={18} />
                Shipping Information
              </h2>
              <div className="space-y-4">
                <div className="grid sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">Full Name</label>
                    <input
                      required
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm"
                      placeholder="John Doe"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">Phone</label>
                    <input
                      required
                      type="tel"
                      pattern="1[3-9]\d{9}"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm"
                      placeholder="13800138000"
                    />
                  </div>
                </div>
                <div className="grid sm:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">Province</label>
                    <select
                      required
                      value={province}
                      onChange={(e) => { setProvince(e.target.value); setCity(''); setDistrict(''); }}
                      className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm bg-white"
                    >
                      <option value="">Select...</option>
                      {PROVINCES.map((p) => (
                        <option key={p} value={p}>{p}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">City</label>
                    <input
                      required
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-neutral-700 mb-1">District</label>
                    <input
                      required
                      value={district}
                      onChange={(e) => setDistrict(e.target.value)}
                      className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-neutral-700 mb-1">Detailed Address</label>
                  <input
                    required
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm"
                    placeholder="Building, street, apartment..."
                  />
                </div>

                {/* Shipping Methods */}
                <div>
                  <label className="block text-sm font-medium text-neutral-700 mb-2">Shipping Method</label>
                  <div className="space-y-2">
                    {SHIPPING_METHODS.map((m) => (
                      <label
                        key={m.id}
                        className={clsx(
                          'flex items-center justify-between p-3 border cursor-pointer transition-all duration-150',
                          shippingMethod === m.id
                            ? 'border-neutral-900 bg-neutral-50'
                            : 'border-neutral-200 hover:border-neutral-400'
                        )}
                      >
                        <div className="flex items-center gap-3">
                          <input
                            type="radio"
                            name="shipping"
                            checked={shippingMethod === m.id}
                            onChange={() => setShippingMethod(m.id)}
                            className="accent-neutral-900"
                          />
                          <div>
                            <p className="text-sm font-medium text-neutral-800">{m.name}</p>
                            <p className="text-xs text-neutral-500">{m.desc}</p>
                          </div>
                        </div>
                        <span className="text-sm font-semibold text-neutral-800">
                          {m.fee === 0 ? 'FREE' : `$${m.fee}`}
                        </span>
                      </label>
                    ))}
                  </div>
                  <p className="text-xs text-neutral-500 mt-2">
                    Free shipping on orders over ${SHIPPING_METHODS[0].freeAbove}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Payment & Promo */}
          {step === 2 && (
            <div className="space-y-6">
              {/* Promo Code */}
              <div className="border border-neutral-200 p-6">
                <h2 className="font-display text-lg font-semibold mb-4">Promo Code</h2>
                <div className="flex gap-2">
                  <input
                    value={promoCode}
                    onChange={(e) => { setPromoCode(e.target.value); setPromoError(''); }}
                    className="flex-1 px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm"
                    placeholder="Enter promo code"
                  />
                  <button
                    type="button"
                    onClick={handleApplyPromo}
                    disabled={!promoCode.trim()}
                    className="px-4 py-2.5 bg-neutral-900 text-white text-sm hover:bg-neutral-700 transition-colors disabled:opacity-40"
                  >
                    Apply
                  </button>
                </div>
                {promoApplied && (
                  <p className="text-sm text-green-600 mt-2">
                    ✓ {promoApplied.code} applied — ${discount} off
                  </p>
                )}
                {promoError && <p className="text-sm text-red-500 mt-2">{promoError}</p>}
              </div>

              {/* Payment Method */}
              <div className="border border-neutral-200 p-6">
                <h2 className="font-display text-lg font-semibold mb-4 flex items-center gap-2">
                  <CreditCard size={18} />
                  Payment Method
                </h2>
                <div className="space-y-2">
                  {PAYMENT_METHODS.map((m) => (
                    <label
                      key={m.id}
                      className={clsx(
                        'flex items-center gap-3 p-3 border cursor-pointer transition-all duration-150',
                        paymentMethod === m.id
                          ? 'border-neutral-900 bg-neutral-50'
                          : 'border-neutral-200 hover:border-neutral-400'
                      )}
                    >
                      <input
                        type="radio"
                        name="payment"
                        checked={paymentMethod === m.id}
                        onChange={() => setPaymentMethod(m.id)}
                        className="accent-neutral-900"
                      />
                      <span className="text-base">{m.icon}</span>
                      <span className="text-sm font-medium text-neutral-800">{m.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Invoice */}
              <div className="border border-neutral-200 p-6">
                <button
                  type="button"
                  onClick={() => setInvoice(!invoice)}
                  className="flex items-center gap-2 text-sm font-medium text-neutral-700"
                >
                  <FileText size={16} />
                  Need an invoice?
                  <span className="text-neutral-400">{invoice ? '(Collapse)' : '(Expand)'}</span>
                </button>
                {invoice && (
                  <div className="mt-3">
                    <input
                      required
                      value={invoiceTitle}
                      onChange={(e) => setInvoiceTitle(e.target.value)}
                      className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm"
                      placeholder="Company name for invoice"
                    />
                  </div>
                )}
              </div>

              {/* Order Notes */}
              <div className="border border-neutral-200 p-6">
                <label className="block text-sm font-medium text-neutral-700 mb-2">Order Notes (Optional)</label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  rows={3}
                  className="w-full px-4 py-2.5 border border-neutral-200 focus:border-neutral-900 outline-none transition-colors text-sm resize-none"
                  placeholder="Any special instructions..."
                />
              </div>
            </div>
          )}

          {/* Step 3: Review */}
          {step === 3 && (
            <div className="space-y-6">
              {/* Address Review */}
              <div className="border border-neutral-200 p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-display text-lg font-semibold">Shipping Address</h2>
                  <button type="button" onClick={goBack} className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">
                    Edit
                  </button>
                </div>
                <p className="text-sm text-neutral-800">
                  {name} · {phone}
                </p>
                <p className="text-sm text-neutral-600 mt-0.5">
                  {province} {city} {district} {address}
                </p>
                <p className="text-xs text-neutral-500 mt-2">
                  {selectedShipping?.name} — {shippingFee === 0 ? 'FREE' : `$${shippingFee}`}
                </p>
              </div>

              {/* Payment Review */}
              <div className="border border-neutral-200 p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="font-display text-lg font-semibold">Payment</h2>
                  <button type="button" onClick={() => setStep(2)} className="text-sm text-neutral-500 hover:text-neutral-900 transition-colors">
                    Edit
                  </button>
                </div>
                <p className="text-sm text-neutral-800">
                  {PAYMENT_METHODS.find((m) => m.id === paymentMethod)?.name}
                </p>
                {invoice && (
                  <p className="text-xs text-neutral-500 mt-1">Invoice: {invoiceTitle}</p>
                )}
              </div>

              {/* Product List */}
              <div className="border border-neutral-200 p-6">
                <h2 className="font-display text-lg font-semibold mb-4">Order Items</h2>
                <ul className="divide-y divide-neutral-100">
                  {items.map((item, i) => (
                    <li key={i} className="flex gap-4 py-3">
                      <img
                        src={item.product.images[0]}
                        alt={item.product.name}
                        className="w-14 h-20 object-cover bg-neutral-100 shrink-0"
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-neutral-800 truncate">{item.product.name}</p>
                        <p className="text-xs text-neutral-500">
                          {item.selectedSize} · {item.selectedColor}
                        </p>
                        <p className="text-xs text-neutral-500">Qty: {item.quantity}</p>
                      </div>
                      <span className="text-sm font-semibold text-neutral-900 shrink-0">
                        ${(item.product.price * item.quantity).toLocaleString()}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Terms */}
              <label className="flex items-start gap-2 text-sm text-neutral-600 cursor-pointer">
                <input
                  type="checkbox"
                  checked={agreed}
                  onChange={(e) => setAgreed(e.target.checked)}
                  className="mt-0.5 accent-neutral-900 shrink-0"
                />
                <span>
                  I agree to the{' '}
                  <a href="#" className="underline text-neutral-900">Terms of Service</a>
                  {' '} and{' '}
                  <a href="#" className="underline text-neutral-900">Privacy Policy</a>
                </span>
              </label>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between pt-4">
            {step > 1 ? (
              <button type="button" onClick={goBack} className="btn-ghost gap-1">
                <ChevronLeft size={16} />
                Back
              </button>
            ) : (
              <button type="button" onClick={() => navigate('/cart')} className="btn-ghost gap-1">
                <ChevronLeft size={16} />
                Back to Cart
              </button>
            )}
            <button
              type="submit"
              disabled={
                submitting ||
                (step === 1 && (!name || !phone || !province || !city || !district || !address)) ||
                (step === 3 && !agreed)
              }
              className="btn-primary gap-2"
            >
              {submitting ? (
                'Processing...'
              ) : step === 3 ? (
                <>
                  Place Order
                  <ChevronRight size={16} />
                </>
              ) : (
                <>
                  Continue
                  <ChevronRight size={16} />
                </>
              )}
            </button>
          </div>
        </form>

        {/* Sidebar: Order Summary (sticky) */}
        <div className="md:sticky md:top-24 h-fit">
          <div className="border border-neutral-200 p-6 space-y-4">
            <h3 className="font-display text-lg font-semibold">Order Summary</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-neutral-600">Subtotal</span>
                <span className="font-medium">${total().toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-neutral-600">Shipping</span>
                <span className="font-medium">
                  {shippingFee === 0 ? (
                    <span className="text-green-600">FREE</span>
                  ) : (
                    `$${shippingFee}`
                  )}
                </span>
              </div>
              {discount > 0 && (
                <div className="flex justify-between text-green-600">
                  <span>Discount ({promoApplied?.code})</span>
                  −${discount.toLocaleString()}
                </div>
              )}
              <div className="border-t border-neutral-200 pt-3 flex justify-between font-semibold text-base">
                <span>Total</span>
                <span>${grandTotal.toLocaleString()}</span>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs text-neutral-500 pt-2 border-t border-neutral-200">
              <Shield size={12} />
              <span>Secure checkout with SSL encryption</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CheckoutPage;
