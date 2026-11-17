import { FormEvent, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Check,
  ChevronLeft,
  ChevronRight,
  CreditCard,
  FileText,
  Landmark,
  Shield,
  Truck,
  Wallet,
} from 'lucide-react';
import { PROMO_CODES } from '../data/products';
import { useCartStore } from '../store/cartStore';
import { FREE_SHIPPING_THRESHOLD, formatPrice } from '../utils/format';
import clsx from 'clsx';

const SHIPPING_METHODS = [
  { id: 'express', name: 'Express courier', desc: '1–2 business days · fully tracked', fee: 15 },
  { id: 'standard', name: 'Standard delivery', desc: '3–5 business days', fee: 8 },
  { id: 'economy', name: 'Economy', desc: '7–10 business days', fee: 0 },
];

const PAYMENT_METHODS = [
  { id: 'card', name: 'Credit or debit card', icon: CreditCard },
  { id: 'wallet', name: 'Digital wallet', icon: Wallet },
  { id: 'bank', name: 'Bank transfer', icon: Landmark },
];

const COUNTRIES = [
  'United States',
  'United Kingdom',
  'Canada',
  'Australia',
  'Germany',
  'France',
  'Netherlands',
  'Japan',
  'Singapore',
  'Other',
];

const STEPS = [
  { n: 1, label: 'Shipping' },
  { n: 2, label: 'Payment' },
  { n: 3, label: 'Review' },
];

function CheckoutPage() {
  const items = useCartStore((state) => state.items);
  const clearCart = useCartStore((state) => state.clearCart);
  const total = useCartStore((state) => state.total);
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [submitting, setSubmitting] = useState(false);
  const [orderId, setOrderId] = useState('');

  // Step 1
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [country, setCountry] = useState('');
  const [city, setCity] = useState('');
  const [postalCode, setPostalCode] = useState('');
  const [address, setAddress] = useState('');
  const [shippingMethod, setShippingMethod] = useState('express');

  // Step 2
  const [promoCode, setPromoCode] = useState('');
  const [promoApplied, setPromoApplied] = useState<{
    code: string;
    discount: number;
    type: 'percent' | 'fixed';
  } | null>(null);
  const [promoError, setPromoError] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [invoice, setInvoice] = useState(false);
  const [invoiceTitle, setInvoiceTitle] = useState('');
  const [notes, setNotes] = useState('');

  // Step 3
  const [agreed, setAgreed] = useState(false);

  useEffect(() => {
    if (items.length === 0 && !orderId) {
      navigate('/cart');
    }
  }, [items, orderId, navigate]);

  const subtotal = total();
  const selectedShipping = SHIPPING_METHODS.find((m) => m.id === shippingMethod);
  const shippingFee = subtotal >= FREE_SHIPPING_THRESHOLD ? 0 : selectedShipping?.fee || 0;
  const discount = promoApplied
    ? promoApplied.type === 'percent'
      ? Math.round((subtotal * promoApplied.discount) / 100)
      : promoApplied.discount
    : 0;
  const grandTotal = Math.max(subtotal + shippingFee - discount, 0);

  const handleApplyPromo = () => {
    setPromoError('');
    const trimmed = promoCode.trim().toUpperCase();
    const found = Object.values(PROMO_CODES).find((c) => c.code === trimmed);
    if (found) {
      setPromoApplied({ code: found.code, discount: found.discount, type: found.type });
    } else {
      setPromoError('That code is not valid or has expired');
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (step < 3) {
      setStep(step + 1);
      return;
    }
    setSubmitting(true);
    await new Promise((r) => setTimeout(r, 1200));
    const id = 'SL' + Date.now().toString(36).toUpperCase();
    setOrderId(id);
    // Cart is cleared only after the customer confirms on the review step.
    clearCart();
    setSubmitting(false);
  };

  const goBack = () => {
    if (step > 1) setStep(step - 1);
  };

  if (orderId) {
    return (
      <div className="mx-auto min-h-screen max-w-screen-xl px-4 py-24 text-center sm:px-6">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-fresh-100">
          <Check size={28} className="text-fresh-600" />
        </div>
        <h1 className="mb-2 font-display text-3xl font-bold">Order placed</h1>
        <p className="mb-1 text-neutral-500">Order number: {orderId}</p>
        <p className="mb-8 text-sm text-neutral-400">
          Thank you. Your order should arrive within 1–3 business days and tracking will be sent to your email.
        </p>
        <div className="flex items-center justify-center gap-4">
          <button onClick={() => navigate('/shop')} className="btn-primary">
            Continue shopping
          </button>
          <button onClick={() => navigate('/')} className="btn-outline">
            Back to home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto min-h-screen max-w-screen-xl px-4 py-10 pt-24 sm:px-6">
      {/* Stepper */}
      <div className="mb-12 flex items-center justify-center gap-3">
        {STEPS.map((s) => (
          <div key={s.n} className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div
                className={clsx(
                  'flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold transition-all duration-300',
                  step > s.n
                    ? 'bg-fresh-600 text-white'
                    : step === s.n
                    ? 'bg-brand-600 text-white'
                    : 'bg-neutral-100 text-neutral-400'
                )}
              >
                {step > s.n ? <Check size={14} /> : s.n}
              </div>
              <span
                className={clsx(
                  'hidden text-sm font-medium sm:inline',
                  step >= s.n ? 'text-neutral-900' : 'text-neutral-400'
                )}
              >
                {s.label}
              </span>
            </div>
            {s.n < 3 && (
              <div className={clsx('h-0.5 w-8 transition-all duration-300', step > s.n ? 'bg-fresh-600' : 'bg-neutral-200')} />
            )}
          </div>
        ))}
      </div>

      <div className="grid gap-8 md:grid-cols-3">
        {/* Main form */}
        <form onSubmit={handleSubmit} className="space-y-6 md:col-span-2">
          {step === 1 && (
            <div className="rounded-2xl border border-neutral-200 p-6">
              <h2 className="mb-6 flex items-center gap-2 font-display text-lg font-semibold">
                <Truck size={18} />
                Shipping details
              </h2>
              <div className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-1 block text-sm font-medium text-neutral-700">Full name</label>
                    <input
                      required
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="input-field"
                      placeholder="Jane Doe"
                    />
                  </div>
                  <div>
                    <label className="mb-1 block text-sm font-medium text-neutral-700">Email</label>
                    <input
                      required
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="input-field"
                      placeholder="you@email.com"
                    />
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-3">
                  <div>
                    <label className="mb-1 block text-sm font-medium text-neutral-700">Country</label>
                    <select
                      required
                      value={country}
                      onChange={(e) => setCountry(e.target.value)}
                      className="input-field"
                    >
                      <option value="">Select a country</option>
                      {COUNTRIES.map((c) => (
                        <option key={c} value={c}>
                          {c}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="mb-1 block text-sm font-medium text-neutral-700">City</label>
                    <input
                      required
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      className="input-field"
                      placeholder="City"
                    />
                  </div>
                  <div>
                    <label className="mb-1 block text-sm font-medium text-neutral-700">Postal code</label>
                    <input
                      required
                      value={postalCode}
                      onChange={(e) => setPostalCode(e.target.value)}
                      className="input-field"
                      placeholder="Postal code"
                    />
                  </div>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium text-neutral-700">Street address</label>
                  <input
                    required
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    className="input-field"
                    placeholder="Street, building, apartment"
                  />
                </div>

                {/* Shipping methods */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-neutral-700">Shipping method</label>
                  <div className="space-y-2">
                    {SHIPPING_METHODS.map((m) => (
                      <label
                        key={m.id}
                        className={clsx(
                          'flex cursor-pointer items-center justify-between rounded-xl border p-3 transition-all duration-150',
                          shippingMethod === m.id
                            ? 'border-brand-600 bg-brand-50'
                            : 'border-neutral-200 hover:border-brand-300'
                        )}
                      >
                        <div className="flex items-center gap-3">
                          <input
                            type="radio"
                            name="shipping"
                            checked={shippingMethod === m.id}
                            onChange={() => setShippingMethod(m.id)}
                            className="accent-brand-600"
                          />
                          <div>
                            <p className="text-sm font-medium text-neutral-800">{m.name}</p>
                            <p className="text-xs text-neutral-500">{m.desc}</p>
                          </div>
                        </div>
                        <span className="text-sm font-semibold text-neutral-800">
                          {m.fee === 0 ? 'Free' : formatPrice(m.fee)}
                        </span>
                      </label>
                    ))}
                  </div>
                  <p className="mt-2 text-xs text-neutral-500">
                    Free shipping on orders over {formatPrice(FREE_SHIPPING_THRESHOLD)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6">
              <div className="rounded-2xl border border-neutral-200 p-6">
                <h2 className="mb-4 font-display text-lg font-semibold">Promo code</h2>
                <div className="flex gap-2">
                  <input
                    value={promoCode}
                    onChange={(e) => {
                      setPromoCode(e.target.value);
                      setPromoError('');
                    }}
                    className="input-field flex-1"
                    placeholder="Enter a promo code"
                  />
                  <button
                    type="button"
                    onClick={handleApplyPromo}
                    disabled={!promoCode.trim()}
                    className="rounded-xl bg-brand-600 px-4 py-2.5 text-sm text-white transition-colors hover:bg-brand-700 disabled:opacity-40"
                  >
                    Apply
                  </button>
                </div>
                {promoApplied && (
                  <p className="mt-2 flex items-center gap-1 text-sm text-fresh-700">
                    <Check size={14} />
                    {promoApplied.code} applied — {formatPrice(discount)} off
                  </p>
                )}
                {promoError && <p className="mt-2 text-sm text-red-500">{promoError}</p>}
              </div>

              <div className="rounded-2xl border border-neutral-200 p-6">
                <h2 className="mb-4 flex items-center gap-2 font-display text-lg font-semibold">
                  <CreditCard size={18} />
                  Payment method
                </h2>
                <div className="space-y-2">
                  {PAYMENT_METHODS.map((m) => (
                    <label
                      key={m.id}
                      className={clsx(
                        'flex cursor-pointer items-center gap-3 rounded-xl border p-3 transition-all duration-150',
                        paymentMethod === m.id
                          ? 'border-brand-600 bg-brand-50'
                          : 'border-neutral-200 hover:border-brand-300'
                      )}
                    >
                      <input
                        type="radio"
                        name="payment"
                        checked={paymentMethod === m.id}
                        onChange={() => setPaymentMethod(m.id)}
                        className="accent-brand-600"
                      />
                      <m.icon size={18} className="text-neutral-700" />
                      <span className="text-sm font-medium text-neutral-800">{m.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="rounded-2xl border border-neutral-200 p-6">
                <button
                  type="button"
                  onClick={() => setInvoice(!invoice)}
                  className="flex items-center gap-2 text-sm font-medium text-neutral-700"
                >
                  <FileText size={16} />
                  Need an invoice?
                  <span className="text-neutral-400">{invoice ? '(hide)' : '(show)'}</span>
                </button>
                {invoice && (
                  <div className="mt-3">
                    <input
                      required
                      value={invoiceTitle}
                      onChange={(e) => setInvoiceTitle(e.target.value)}
                      className="input-field"
                      placeholder="Invoice title (company name)"
                    />
                  </div>
                )}
              </div>

              <div className="rounded-2xl border border-neutral-200 p-6">
                <label className="mb-2 block text-sm font-medium text-neutral-700">Order notes (optional)</label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  rows={3}
                  className="input-field resize-none"
                  placeholder="Add a delivery preference if you have one"
                />
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6">
              <div className="rounded-2xl border border-neutral-200 p-6">
                <div className="mb-4 flex items-center justify-between">
                  <h2 className="font-display text-lg font-semibold">Shipping address</h2>
                  <button
                    type="button"
                    onClick={goBack}
                    className="text-sm text-neutral-500 transition-colors hover:text-brand-600"
                  >
                    Edit
                  </button>
                </div>
                <p className="text-sm text-neutral-800">
                  {name} · {email}
                </p>
                <p className="mt-0.5 text-sm text-neutral-600">
                  {address}, {city} {postalCode}, {country}
                </p>
                <p className="mt-2 text-xs text-neutral-500">
                  {selectedShipping?.name} — {shippingFee === 0 ? 'Free' : formatPrice(shippingFee)}
                </p>
              </div>

              <div className="rounded-2xl border border-neutral-200 p-6">
                <div className="mb-4 flex items-center justify-between">
                  <h2 className="font-display text-lg font-semibold">Payment method</h2>
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="text-sm text-neutral-500 transition-colors hover:text-brand-600"
                  >
                    Edit
                  </button>
                </div>
                <p className="text-sm text-neutral-800">
                  {PAYMENT_METHODS.find((m) => m.id === paymentMethod)?.name}
                </p>
                {invoice && <p className="mt-1 text-xs text-neutral-500">Invoice title: {invoiceTitle}</p>}
                {notes && <p className="mt-1 text-xs text-neutral-500">Notes: {notes}</p>}
              </div>

              <div className="rounded-2xl border border-neutral-200 p-6">
                <h2 className="mb-4 font-display text-lg font-semibold">Items</h2>
                <ul className="divide-y divide-neutral-100">
                  {items.map((item, i) => (
                    <li key={i} className="flex gap-4 py-3">
                      <img
                        src={item.product.images[0]}
                        alt={item.product.name}
                        className="h-20 w-14 shrink-0 rounded-lg bg-neutral-100 object-cover"
                      />
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium text-neutral-800">{item.product.name}</p>
                        <p className="text-xs text-neutral-500">
                          {item.selectedSize} · {item.selectedColor}
                        </p>
                        <p className="text-xs text-neutral-500">Qty: {item.quantity}</p>
                      </div>
                      <span className="shrink-0 text-sm font-semibold text-neutral-900">
                        {formatPrice(item.product.price * item.quantity)}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              <label className="flex cursor-pointer items-start gap-2 text-sm text-neutral-600">
                <input
                  type="checkbox"
                  checked={agreed}
                  onChange={(e) => setAgreed(e.target.checked)}
                  className="mt-0.5 shrink-0 accent-brand-600"
                />
                <span>
                  I have read and agree to the
                  <a href="#" className="mx-1 text-brand-600 underline">
                    terms of service
                  </a>
                  and
                  <a href="#" className="mx-1 text-brand-600 underline">
                    privacy policy
                  </a>
                </span>
              </label>
            </div>
          )}

          {/* Navigation */}
          <div className="flex items-center justify-between pt-4">
            {step > 1 ? (
              <button type="button" onClick={goBack} className="btn-ghost">
                <ChevronLeft size={16} />
                Back
              </button>
            ) : (
              <button type="button" onClick={() => navigate('/cart')} className="btn-ghost">
                <ChevronLeft size={16} />
                Back to cart
              </button>
            )}
            <button
              type="submit"
              disabled={
                submitting ||
                (step === 1 && (!name || !email || !country || !city || !postalCode || !address)) ||
                (step === 3 && !agreed)
              }
              className="btn-primary"
            >
              {submitting ? (
                'Submitting...'
              ) : step === 3 ? (
                <>
                  Place order
                  <ChevronRight size={16} />
                </>
              ) : (
                <>
                  Next
                  <ChevronRight size={16} />
                </>
              )}
            </button>
          </div>
        </form>

        {/* Sticky summary */}
        <div className="h-fit md:sticky md:top-24">
          <div className="space-y-4 rounded-2xl border border-neutral-200 p-6">
            <h3 className="font-display text-lg font-semibold">Order summary</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-neutral-600">Subtotal</span>
                <span className="font-medium">{formatPrice(subtotal)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-neutral-600">Shipping</span>
                <span className="font-medium">
                  {shippingFee === 0 ? <span className="text-fresh-600">Free</span> : formatPrice(shippingFee)}
                </span>
              </div>
              {discount > 0 && (
                <div className="flex justify-between text-fresh-700">
                  <span>Discount ({promoApplied?.code})</span>
                  <span>−{formatPrice(discount)}</span>
                </div>
              )}
              <div className="flex justify-between border-t border-neutral-200 pt-3 text-base font-semibold">
                <span>Total due</span>
                <span>{formatPrice(grandTotal)}</span>
              </div>
            </div>
            <div className="flex items-center gap-2 border-t border-neutral-200 pt-2 text-xs text-neutral-500">
              <Shield size={12} />
              <span>Encrypted end to end — we never store your payment details</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CheckoutPage;
