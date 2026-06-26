import { Instagram, Twitter, Youtube } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-neutral-900 text-neutral-400 mt-auto">
      <div className="max-w-screen-xl mx-auto px-4 sm:px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-12">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <h3 className="font-display text-white text-xl tracking-[0.15em] uppercase mb-4">__SITE_NAME__</h3>
            <p className="text-sm leading-relaxed mb-6">
              Premium products by __BRAND_NAME__. Crafted with passion and attention to detail.
            </p>
            <div className="flex gap-4">
              <a href="#" className="hover:text-white transition-colors" aria-label="Instagram">
                <Instagram size={18} />
              </a>
              <a href="#" className="hover:text-white transition-colors" aria-label="Twitter">
                <Twitter size={18} />
              </a>
              <a href="#" className="hover:text-white transition-colors" aria-label="Youtube">
                <Youtube size={18} />
              </a>
            </div>
          </div>

          {/* Shop */}
          <div>
            <h4 className="text-white text-xs tracking-widest uppercase mb-4">Shop</h4>
            <ul className="space-y-3 text-sm">
              {['New Arrivals', 'Bestsellers', 'Sale', 'Limited Edition'].map((i) => (
                <li key={i}>
                  <a href="#" className="hover:text-white transition-colors">{i}</a>
                </li>
              ))}
            </ul>
          </div>

          {/* Help */}
          <div>
            <h4 className="text-white text-xs tracking-widest uppercase mb-4">Help</h4>
            <ul className="space-y-3 text-sm">
              {['Size Guide', 'Shipping Info', 'Returns Policy', 'Contact Us'].map((i) => (
                <li key={i}>
                  <a href="#" className="hover:text-white transition-colors">{i}</a>
                </li>
              ))}
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h4 className="text-white text-xs tracking-widest uppercase mb-4">Newsletter</h4>
            <p className="text-sm mb-4">Be the first to know about new arrivals and exclusive offers.</p>
            <div className="flex">
              <input
                type="email"
                placeholder="Your email"
                className="flex-1 px-4 py-2.5 bg-neutral-800 text-white text-sm placeholder-neutral-500 outline-none border border-neutral-700 focus:border-neutral-500 transition-colors"
              />
              <button className="px-4 py-2.5 bg-white text-neutral-900 text-sm font-medium hover:bg-neutral-100 transition-colors whitespace-nowrap">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        <div className="border-t border-neutral-800 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
          <p>&copy; {new Date().getFullYear()} __BRAND_NAME__. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-white transition-colors">Cookie Settings</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
