# Free Static Hosting for Identity Card

Publish your OpenClaw identity card to a **public free site** without running a server. All platforms below offer free tiers suitable for a single HTML page.

---

## Comparison

| Platform | Free URL | Setup | Notes |
|----------|----------|-------|-------|
| **GitHub Pages** | `username.github.io/repo` | Git push | Simplest if you use GitHub |
| **Netlify** | `sitename.netlify.app` | Git or drag-drop | Deploy previews, forms |
| **Vercel** | `project.vercel.app` | Git | Good for Next.js, also static |
| **Cloudflare Pages** | `project.pages.dev` | Git | Fast CDN, Workers |

---

## GitHub Pages (Recommended for Beginners)

### Step 1: Create Repo

1. Go to [github.com/new](https://github.com/new)
2. Repo name: e.g. `my-identity` or `username.github.io` (for root URL)
3. Public, no README

### Step 2: Push HTML

```bash
git clone https://github.com/username/my-identity.git
cd my-identity
# Copy your index.html here
git add index.html
git commit -m "Add identity card"
git push origin main
```

### Step 3: Enable Pages

1. Repo → Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: `main` (or `master`), folder: `/ (root)`
4. Save

### Step 4: Access

- Project repo: `https://username.github.io/my-identity/`
- User site (`username.github.io` repo): `https://username.github.io/`

---

## Netlify (Drag-and-Drop)

1. Go to [app.netlify.com](https://app.netlify.com)
2. Sign up (free, GitHub/email)
3. **Add new site** → **Deploy manually**
4. Drag folder containing `index.html` to drop zone
5. Get URL: `random-name.netlify.app`
6. (Optional) Site settings → Change site name → `my-identity` → `my-identity.netlify.app`

---

## Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up (GitHub recommended)
3. **Add New Project** → Import Git repo
4. Framework: Other (static)
5. Deploy → get `project.vercel.app`

---

## Cloudflare Pages

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com) → Pages
2. **Create project** → Connect to Git (or Direct Upload)
3. Build: None (static)
4. Output directory: `/`
5. Deploy → get `project.pages.dev`

---

## Custom Domain (Optional)

All platforms support custom domains on free tier:
- GitHub Pages: Add CNAME file or configure in Settings
- Netlify/Vercel/Cloudflare: Add domain in dashboard, follow DNS instructions
