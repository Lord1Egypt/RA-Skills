import { Globe, Headphones, Instagram, ShieldCheck, Truck, Twitter, Youtube } from 'lucide-react';
import { Link } from 'react-router-dom';
import { categories } from '../data/products';

const serviceBanner = [
  { icon: Truck, title: 'Free shipping', desc: 'Free delivery on orders over ¥299' },
  { icon: ShieldCheck, title: 'Guaranteed quality', desc: 'Authorised sourcing · money back if not genuine' },
  { icon: Globe, title: 'Sourced globally', desc: 'Every fabric traceable to its mill' },
  { icon: Headphones, title: 'Dedicated support', desc: 'Online 10:00–22:00' },
];

const helpLinks = ['Size guide', 'Shipping', 'Returns', 'Contact us'];

export default function Footer() {
  return (
    <footer className="mt-auto bg-neutral-900 text-neutral-400">
      {/* Service banner */}
      <div className="mx-auto max-w-screen-xl px-4 py-10 sm:px-6">
        <div className="grid grid-cols-2 gap-6 md:grid-cols-4">
          {serviceBanner.map((s) => (
            <div key={s.title} className="flex items-start gap-3">
              <s.icon size={20} className="mt-0.5 shrink-0 text-brand-300" />
              <div>
                <p className="text-sm font-medium text-white">{s.title}</p>
                <p className="mt-0.5 text-xs text-neutral-500">{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mx-auto max-w-screen-xl px-4 pb-16 sm:px-6">
        <div className="grid grid-cols-2 gap-10 border-t border-neutral-800 pt-12 md:grid-cols-4">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <h3 className="mb-4 font-display text-xl uppercase tracking-[0.15em] text-white">
              __SITE_NAME__
            </h3>
            <p className="mb-6 text-sm leading-relaxed">
              __BRAND_NAME__ is about fabric and cut — everyday pieces built to be judged over time.
            </p>
            <div className="flex gap-4">
              <a href="#" className="transition-colors hover:text-white" aria-label="Instagram">
                <Instagram size={18} />
              </a>
              <a href="#" className="transition-colors hover:text-white" aria-label="Twitter">
                <Twitter size={18} />
              </a>
              <a href="#" className="transition-colors hover:text-white" aria-label="Youtube">
                <Youtube size={18} />
              </a>
            </div>
          </div>

          {/* Categories */}
          <div>
            <h4 className="mb-4 text-xs uppercase tracking-widest text-white">Shop</h4>
            <ul className="space-y-3 text-sm">
              {categories
                .filter((c) => c.key !== 'all')
                .map((c) => (
                  <li key={c.key}>
                    <Link to={`/shop?category=${c.key}`} className="transition-colors hover:text-white">
                      {c.label}
                    </Link>
                  </li>
                ))}
            </ul>
          </div>

          {/* Help */}
          <div>
            <h4 className="mb-4 text-xs uppercase tracking-widest text-white">Help</h4>
            <ul className="space-y-3 text-sm">
              {helpLinks.map((i) => (
                <li key={i}>
                  <a href="#" className="transition-colors hover:text-white">
                    {i}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h4 className="mb-4 text-xs uppercase tracking-widest text-white">Newsletter</h4>
            <p className="mb-4 text-sm">Be first to hear about new arrivals and private offers.</p>
            <div className="flex">
              <input
                type="email"
                placeholder="Your email"
                className="flex-1 border border-neutral-700 bg-neutral-800 px-4 py-2.5 text-sm text-white outline-none transition-colors placeholder:text-neutral-500 focus:border-neutral-500"
              />
              <button className="whitespace-nowrap bg-white px-4 py-2.5 text-sm font-medium text-neutral-900 transition-colors hover:bg-neutral-100">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-neutral-800 pt-8 text-xs sm:flex-row">
          <p>© {new Date().getFullYear()} __BRAND_NAME__. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="#" className="transition-colors hover:text-white">Privacy policy</a>
            <a href="#" className="transition-colors hover:text-white">Terms of service</a>
            <a href="#" className="transition-colors hover:text-white">Cookie settings</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
