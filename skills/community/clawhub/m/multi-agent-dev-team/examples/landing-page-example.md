# Example: Next.js Landing Page

This is a real example of a project completed using the Multi-Agent Dev Team.

## Request (from Director to PM)

```markdown
Build a Next.js landing page with the following:

**Sections:**
- Hero section with headline, subheadline, and CTA button
- Features section with 3 feature cards
- Contact section with CTA

**Tech Requirements:**
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Fully responsive design
```

## PM Agent Response

The PM agent created this task specification for the Dev agent:

```markdown
## Project: Next.js Landing Page Development
## Task: Build a responsive landing page with Hero, Features, and Contact sections

## Requirements:
1. Use Next.js 14+ with App Router architecture
2. Implement TypeScript for type safety
3. Use Tailwind CSS for styling
4. Create three main sections: Hero, Features, Contact
5. Ensure fully responsive design (mobile-first approach)
6. Include reusable components

## Technical Constraints:
- Framework: Next.js 16.1.6 or later
- Language: TypeScript
- Styling: Tailwind CSS 4
- Component Architecture: Modular, reusable components

## Acceptance Criteria:
- [ ] Next.js project initialized with App Router
- [ ] TypeScript configured correctly
- [ ] Tailwind CSS integrated
- [ ] Hero section with headline, subheadline, and CTA button
- [ ] Features section with at least 3 feature cards
- [ ] Contact section with CTA
- [ ] Responsive design working on mobile, tablet, and desktop
- [ ] Clean, readable code with proper component structure
- [ ] Git repository initialized with initial commit

## Deliverables:
- Working Next.js application
- Source code in project directory
- README with setup instructions
- Git repository with clean commit history
```

## Dev Agent Implementation

The Dev agent created the following structure:

```
my-landing-page/
├── app/
│   ├── layout.tsx          # Root layout with Inter font
│   ├── page.tsx             # Main page importing sections
│   └── globals.css          # Global styles + Tailwind
├── components/
│   ├── sections/
│   │   ├── HeroSection.tsx
│   │   ├── FeaturesSection.tsx
│   │   └── ContactSection.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   └── ui/
│       └── Button.tsx       # Reusable button with variants
├── lib/
│   └── utils.ts             # Utility functions (cn helper)
├── package.json
├── tsconfig.json
├── next.config.ts
└── README.md
```

### Key Implementation Details

**1. Component Architecture**
- Modular sections (Hero, Features, Contact)
- Reusable UI components (Button)
- Layout components (Header, Footer)
- Utility functions for class management

**2. Styling**
- Tailwind CSS with custom theme
- Responsive breakpoints
- Dark mode support (via CSS variables)
- Modern gradient backgrounds

**3. TypeScript**
- Full type safety
- Proper type definitions for components
- No `any` types

**4. Best Practices**
- Semantic HTML
- Accessible components
- SEO-friendly metadata
- Clean code structure

## QA Results

The PM agent coordinated QA which found:

### ✅ Strengths
- Excellent adherence to Next.js 14+ patterns
- Clean, modular code structure
- Proper TypeScript usage
- Good Tailwind CSS implementation
- Responsive design implemented

### ⚠️ Minor Issues
1. Missing `key` prop in Features section map
2. Could use `min-h-screen` instead of `h-screen` for better small screen support
3. Font consistency between `globals.css` and `layout.tsx`

### 📦 Dependencies
- 15 npm audit vulnerabilities found
- All in devDependencies (eslint-related)
- No production impact

**Final Verdict:** ✅ **PASS** (with minor improvements recommended)

## Deployment

The DevOps agent (in Pro version) deployed to:
- **GitHub**: https://github.com/ubikcollectivereal/my-landing-page
- **Vercel**: https://my-landing-page-blush-rho.vercel.app

### Deployment Steps
1. Created GitHub repository
2. Pushed code with proper commit messages
3. Connected to Vercel
4. Fixed TypeScript build error (Button component)
5. Deployed to production
6. Verified live site

## Timeline

- **Request to PM:** 0 minutes
- **PM → Dev handoff:** 2 minutes (task spec creation)
- **Dev implementation:** 15 minutes
- **QA review:** 5 minutes (automated + manual)
- **Deployment:** 3 minutes

**Total:** ~25 minutes from request to live site 🚀

## Lessons Learned

### What Worked Well
✅ Clear initial requirements
✅ Modular component structure
✅ TypeScript from the start
✅ Multi-agent collaboration (PM → Dev → QA → DevOps)

### What Could Improve
⚠️ More specific design requirements (colors, fonts)
⚠️ Explicitly request key props in loops
⚠️ Specify min-h-screen preference upfront

### Recommendations
1. Provide design mockups or references when available
2. Specify code quality requirements explicitly
3. Request specific testing (e.g., "ensure all array maps have key props")
4. Consider QA as a separate step (use Pro for automated QA)

## How to Replicate

Want to build something similar?

```markdown
Hey PM, build me a Next.js landing page similar to the example,
but for [YOUR PRODUCT NAME].

Features:
- Hero section with [YOUR HEADLINE]
- Features showcasing [YOUR TOP 3 FEATURES]
- Contact section encouraging [YOUR CTA]

Tech: Next.js 14+, TypeScript, Tailwind CSS

Design: [YOUR COLOR SCHEME, any specific style preferences]
```

Then sit back and let the agents work! ✨

## Source Code

The complete source code for this example is available on GitHub:
https://github.com/ubikcollectivereal/my-landing-page

## Live Demo

See the deployed result:
https://my-landing-page-blush-rho.vercel.app

---

**This example demonstrates the power of multi-agent collaboration!** With just a simple request, multiple AI agents worked together to design, build, test, and deploy a complete landing page.

Ready to build your own? [Install the skill →](#quick-start)
