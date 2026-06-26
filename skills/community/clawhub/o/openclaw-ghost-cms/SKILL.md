# Ghost CMS Skill

A comprehensive skill for Ghost CMS development, theme creation, and management.

## Description

This skill provides complete Ghost CMS development support including installation, theme development with Handlebars, Ghost CLI commands, API integration (Content and Admin APIs), GScan validation, custom theme settings, dynamic routing, local development workflows, publishing, and deployment best practices.

## Usage

Use this skill when you need help with:

- Installing and configuring Ghost (local and production)
- Using Ghost CLI commands for site management
- Creating and customizing Ghost themes with Handlebars
- Working with theme helpers (data, functional, utility)
- Setting up theme structure and templates
- Implementing custom theme settings
- Using Content API and Admin API
- Validating themes with GScan
- Managing assets and images
- Implementing dynamic routing with routes.yaml
- Setting up local development workflow
- Publishing and deploying themes
- Troubleshooting Ghost issues
- Security and performance optimization

## Commands & Tools

### Installation & Setup

```bash
# Install Ghost CLI globally
npm install -g ghost-cli@latest

# Install Ghost locally for development
ghost install local

# Install Ghost in production
ghost install
```

### Essential Ghost CLI Commands

```bash
ghost start      # Start Ghost
ghost stop       # Stop Ghost
ghost restart    # Restart Ghost
ghost update     # Update Ghost to latest version
ghost ls         # List Ghost instances
ghost log        # View logs
```

### Theme Development

#### Required Theme Structure
```
your-theme/
├── assets/
│   ├── css/
│   ├── fonts/
│   ├── images/
│   └── js/
├── partials/
│   ├── header.hbs
│   └── footer.hbs
├── default.hbs       # Base layout
├── index.hbs        # Required - post list
├── post.hbs         # Required - single post
├── page.hbs         # Static pages
├── tag.hbs          # Tag archive
├── author.hbs        # Author archive
├── error.hbs        # Error pages
└── package.json     # Required - theme metadata
```

#### Required Helpers (Must Include)
```handlebars
{{ghost_head}}     <!-- In <head> section -->
{{ghost_foot}}     <!-- Before </body> -->
{{body_class}}     <!-- Dynamic body classes -->
{{asset "path"}}   <!-- Link to theme assets -->
```

#### Common Data Helpers
```handlebars
{{#post}}...{{/post}}              <!-- Post context -->
{{#foreach posts}}...{{/foreach}}  <!-- Loop posts -->
{{title}}                         <!-- Page/post title -->
{{content}}                       <!-- Post content -->
{{excerpt}}                       <!-- Post excerpt -->
{{date format="YYYY-MM-DD"}}       <!-- Format dates -->
{{img_url feature_image}}          <!-- Image URL -->
{{url}}                           <!-- Current page URL -->
{{navigation}}                    <!-- Main navigation -->
{{pagination}}                    <!-- Pagination links -->
```

#### Custom Templates
```handlebars
<!-- Post-specific: post-my-slug.hbs -->
<!-- Page-specific: page-about.hbs -->
<!-- Tag-specific: tag-javascript.hbs -->
<!-- Author-specific: author-john.hbs -->
```

### package.json Configuration

```json
{
  "name": "your-theme-name",
  "version": "1.0.0",
  "description": "Brief description",
  "license": "MIT",
  "author": {
    "name": "Your Name",
    "email": "your@email.com"
  },
  "screenshots": {
    "desktop": "assets/screenshot-desktop.jpg",
    "mobile": "assets/screenshot-mobile.jpg"
  },
  "config": {
    "posts_per_page": 10,
    "image_sizes": {
      "xxl": { "width": 2000 },
      "xl": { "width": 1200 },
      "lg": { "width": 1000 },
      "md": { "width": 800 },
      "sm": { "width": 600 },
      "xs": { "width": 300 }
    },
    "card_assets": true,
    "custom": {
      "color_scheme": {
        "type": "select",
        "default": "Light",
        "options": ["Light", "Dark", "Auto"]
      },
      "accent_color": {
        "type": "color",
        "default": "#3eb0ef"
      }
    }
  }
}
```

### Content API Usage

```javascript
// Install
npm install @tryghost/content-api

// Initialize
const GhostContentAPI = require('@tryghost/content-api');

const api = new GhostContentAPI({
  url: 'https://your-site.com',
  key: 'content_api_key',
  version: 'v5.0'
});

// Fetch posts
api.posts.browse({limit: 5, include: 'tags,authors'})
  .then((posts) => {
    posts.forEach((post) => console.log(post.title));
  });

// Filter posts
api.posts.browse({
  filter: 'tag:javascript+featured:true',
  limit: 10
});

// Fetch single post
api.posts.read({slug: 'post-slug'});
```

### Admin API - Complete Reference

The Admin API provides comprehensive content management capabilities with three authentication methods:

#### Authentication Methods

**1. Integration Token Authentication** (Recommended for server-side apps)
- Create Custom Integration in Ghost Admin
- Get Admin API key (id:secret format)
- Tokens last 5 minutes
- Generate JWT tokens server-side only

**2. Staff Access Token Authentication** (For specific users)
- Each user creates their own token in settings
- Authenticates with role-based permissions
- Tokens are short-lived JWTs
- Suitable for user-specific applications

**3. User Authentication** (For browser apps with login)
- Email + password → session cookie
- Requires 2FA support
- Must include Origin header (CSRF protection)
- Safe for browser environments

#### Available Endpoints (All stable)

| Resource | Methods | Description |
|----------|----------|-------------|
| `/posts/` | Browse, Read, Edit, Add, Copy, Delete | Full post management |
| `/pages/` | Browse, Read, Edit, Add, Copy, Delete | Static page management |
| `/tags/` | Browse, Read, Edit, Add, Delete | Tag management |
| `/tiers/` | Browse, Read, Edit, Add | Membership tier management |
| `/newsletters/` | Browse, Read, Edit, Add | Newsletter management |
| `/offers/` | Browse, Read, Edit, Add | Discount offers for members |
| `/members/` | Browse, Read, Edit, Add | Member management with subscriptions |
| `/users/` | Browse, Read | User management |
| `/images/` | Upload | Image upload and storage |
| `/themes/` | Upload, Activate | Theme management |
| `/site/` | Read | Site configuration |
| `/webhooks/` | Edit, Add, Delete | Webhook configuration |

#### Token Generation Examples

**Bash with OpenSSL:**
```bash
#!/usr/bin/env bash

KEY="YOUR_ADMIN_API_KEY"
IFS=':' read ID SECRET <<< "$KEY"

NOW=$(date +'%s')
FIVE_MINS=$(($NOW + 300))
HEADER="{\"alg\": \"HS256\",\"typ\": \"JWT\", \"kid\": \"$ID\"}"
PAYLOAD="{\"iat\":$NOW,\"exp\":$FIVE_MINS,\"aud\": \"/admin/\"}"

base64_url_encode() {
  printf '%s' "${1}" | base64 | tr -d '=' | tr '+' '-' | tr '/' '_'
}

header_base64=$(base64_url_encode "$HEADER")
payload_base64=$(base64_url_encode "$PAYLOAD")

header_payload="${header_base64}.${payload_base64}"
signature=$(printf '%s' "${header_payload}" | openssl dgst -binary -sha256 -mac HMAC -macopt hexkey:$SECRET | base64_url_encode)

TOKEN="${header_payload}.${signature}"
curl -H "Authorization: Ghost $TOKEN" -H "Content-Type: application/json" \
  -d '{"posts":[{"title":"Hello world"}]}' \
  "http://localhost:2368/ghost/api/admin/posts/"
```

**JavaScript (without client library):**
```javascript
const jwt = require('jsonwebtoken');
const axios = require('axios');

const key = 'YOUR_ADMIN_API_KEY';
const [id, secret] = key.split(':');

const token = jwt.sign({}, Buffer.from(secret, 'hex'), {
  keyid: id,
  algorithm: 'HS256',
  expiresIn: '5m',
  audience: `/admin/`
});

const url = 'http://localhost:2368/ghost/api/admin/posts/';
const headers = { Authorization: `Ghost ${token}` };
const payload = { posts: [{ title: 'Hello World' }] };
axios.post(url, payload, { headers })
  .then(response => console.log(response))
  .catch(error => console.error(error));
```

**Python:**
```python
import requests
import jwt
from datetime import datetime

key = 'YOUR_ADMIN_API_KEY'
id, secret = key.split(':')

iat = int(datetime.now().timestamp())
header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
payload = {
  'iat': iat,
  'exp': iat + 5 * 60,
  'aud': '/admin/'
}

token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

url = 'http://localhost:2368/ghost/api/admin/posts/'
headers = {'Authorization': 'Ghost {}'.format(token)}
body = {'posts': [{'title': 'Hello World'}]}
r = requests.post(url, json=body, headers=headers)
print(r)
```

#### Members API

**Create Member:**
```javascript
api.members.add({
  email: 'user@example.com',
  name: 'Jamie',
  labels: [{ name: 'VIP', slug: 'vip' }],
  newsletters: [{ id: 'newsletter_id' }]
});
```

**Update Member:**
```javascript
api.members.edit({
  id: 'member_id',
  name: 'Updated Name',
  note: 'VIP customer'
});
```

**Member Fields:**
- `email` (required)
- `name`
- `note`
- `labels` (array with name and slug)
- `newsletters` (array of IDs)
- `status` (free, paid, comped)

#### Newsletters API

**Create Newsletter:**
```javascript
api.newsletters.add({
  name: 'My Newsletter',
  description: 'Description',
  sender_reply_to: 'newsletter', // or 'support'
  status: 'active',
  subscribe_on_signup: true,
  show_header_icon: true,
  show_header_title: true,
  title_font_category: 'sans_serif',
  title_alignment: 'center',
  show_feature_image: true,
  body_font_category: 'sans_serif',
  show_badge: true
});
```

**Newsletter Fields:**
- `name` (required)
- `description`
- `status` (active, archived)
- `sender_name`
- `sender_email` (requires verification)
- `sender_reply_to` (newsletter, support)
- `subscribe_on_signup`
- `header_image` (1200x600 recommended)
- `show_header_icon`
- `show_header_title`
- `show_header_name`
- `title_font_category` (serif, sans_serif)
- `title_alignment`
- `show_feature_image`
- `body_font_category` (serif, sans_serif)
- `footer_content`
- `show_badge`

#### Offers API

**Create Offer:**
```javascript
api.offers.add({
  name: 'Black Friday',
  code: 'black-friday',
  display_title: 'Black Friday Sale!',
  display_description: '10% off on yearly plan',
  type: 'percent', // or 'fixed'
  cadence: 'year', // or 'month'
  amount: 12, // percentage or cents
  duration: 'once', // 'once', 'forever', 'repeating'
  tier: { id: 'tier_id' },
  status: 'active'
});
```

**Offer Fields:**
- `name` (required, unique)
- `code` (required, short code)
- `display_title`
- `display_description`
- `type` (percent, fixed)
- `cadence` (year, month)
- `amount` (in smallest currency unit)
- `duration` (once, forever, repeating)
- `duration_in_months` (for repeating)
- `currency` (required for fixed type)
- `status` (active, archived)
- `redemption_count`
- `tier` (tier object with id and name)

#### Posts API - Card Visibility

Control who sees specific cards in posts:

```javascript
// Card with visibility controls
const postWithVisibility = {
  title: 'Premium Content',
  lexical: {
    root: {
      type: 'root',
      children: [
        {
          type: 'html',
          html: '<div>Premium analysis...</div>',
          visibility: {
            web: {
              nonMember: false,
              memberSegment: 'status:free,status:-free'
            },
            email: {
              memberSegment: 'status:free'
            }
          }
        }
      ]
    }
  }
};
```

**Visibility Options:**
- `web.nonMember`: true/false (visible to non-members)
- `web.memberSegment`: NQL filter (e.g., "status:free" for all members, "status:-free" for paid only)
- `email.memberSegment`: NQL filter for email delivery

**Common Configurations:**

Visible to all members (free and paid), hidden from non-members:
```json
{
  "visibility": {
    "web": { "nonMember": false, "memberSegment": "status:free,status:-free" },
    "email": { "memberSegment": "status:free,status:-free" }
  }
}
```

Visible to paid members only:
```json
{
  "visibility": {
    "web": { "nonMember": false, "memberSegment": "status:-free" },
    "email": { "memberSegment": "status:-free" }
  }
}
```

#### Images API

**Upload Image:**
```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('/path/to/image.jpg'));
form.append('ref', 'path/to/image.jpg');
form.append('purpose', 'image'); // 'image', 'profile_image', or 'icon'

fetch('http://localhost:2368/ghost/api/admin/images/upload/', {
  method: 'POST',
  headers: {
    'Authorization': `Ghost ${token}`,
    'Accept-Version': 'v5.0'
  },
  body: form
})
  .then(res => res.json())
  .then(data => console.log(data));
```

**Image Upload Fields:**
- `file` (required) - Blob or File object
- `purpose` - 'image' (default), 'profile_image', or 'icon'
- `ref` (optional) - Reference identifier

**Supported Formats:**
- `image`, `icon`: WEBP, JPEG, GIF, PNG, SVG
- `profile_image`: Must be square, WEBP, JPEG, GIF, PNG, SVG

#### Admin API JavaScript Client

**Installation:**
```bash
npm install @tryghost/admin-api
# or
yarn add @tryghost/admin-api
```

**Usage:**
```javascript
const GhostAdminAPI = require('@tryghost/admin-api');

const api = new GhostAdminAPI({
  url: 'http://localhost:2368/',
  key: 'YOUR_ADMIN_API_KEY',
  version: "v6.0"
});

// Browse posts
api.posts.browse();

// Read post
api.posts.read({id: 'abcd1234'});

// Add post
api.posts.add({
  title: 'My first draft API post',
  lexical: '{"root":{"children":[...]}}' // Lexical JSON structure
});

// Edit post
api.posts.edit({
  id: 'abcd1234',
  title: 'Renamed my post',
  updated_at: post.updated_at
});

// Delete post
api.posts.delete({id: 'abcd1234'});

// Upload image
api.images.upload({
  file: '/path/to/local/file'
});
```

**Complete Publishing Example with Image Processing:**
```javascript
const GhostAdminAPI = require('@tryghost/admin-api');
const path = require('path');
const fs = require('fs');

const api = new GhostAdminAPI({
  url: 'http://localhost:2368/',
  version: "v6.0",
  key: 'YOUR_ADMIN_API_KEY'
});

function processImagesInHTML(html) {
  const imageRegex = /="([^"]*?(?:\.jpg|\.jpeg|\.gif|\.png|\.svg|\.webp))"/gmi;
  const imagePromises = [];

  let result;
  while((result = imageRegex.exec(html)) !== null) {
    const file = result[1];
    imagePromises.push(api.images.upload({
      ref: file,
      file: path.resolve(file)
    }));
  }

  return Promise.all(imagePromises)
    .then(images => {
      images.forEach(image => {
        html = html.replace(image.ref, image.url);
      });
      return html;
    });
}

let html = '<p>My test post content.</p><figure><img src="/path/to/my/image.jpg" /><figcaption>My awesome photo</figcaption></figure>';

processImagesInHTML(html)
  .then(html => {
    return api.posts.add(
      {title: 'My Test Post', html},
      {source: 'html'}
    );
  })
  .then(res => console.log(JSON.stringify(res)))
  .catch(err => console.log(err));
```

#### API Best Practices

1. **Authentication**
   - Use Integration tokens for server-side apps
   - Use Staff tokens for user-specific operations
   - Use User authentication only for browser apps
   - Never expose Admin API keys in client-side code
   - Regenerate tokens periodically (5-minute lifetime)

2. **Pagination**
   - Default limit: 15 records
   - Use `page` and `limit` parameters
   - Check `meta.pagination` for navigation
   - Implement pagination UI based on total/pages

3. **Error Handling**
   - Handle HTTP status codes appropriately
   - Check `meta` for validation errors
   - Implement retry logic for rate limiting
   - Log errors with context

4. **Rate Limiting**
   - Be mindful of API rate limits
   - Implement exponential backoff for retries
   - Cache responses when appropriate

5. **Versioning**
   - Always include `Accept-Version` header
   - Specify minimum API version your code works with
   - Test against different Ghost versions

### Admin API Usage (Server-side)

```javascript
const GhostAdminAPI = require('@tryghost/admin-api');

const api = new GhostAdminAPI({
  url: 'https://your-site.com',
  key: 'admin_api_key',
  version: 'v5.0'
});

// Create post
const post = await api.posts.add({
  title: 'My New Post',
  html: '<p>Content</p>',
  status: 'published'
});

// Update post
await api.posts.edit({
  id: post.id,
  title: 'Updated Title'
});
```

### Custom Theme Settings

Define in package.json:
```json
{
  "config": {
    "custom": {
      "show_featured_posts": {
        "type": "boolean",
        "default": true
      },
      "posts_per_page": {
        "type": "select",
        "default": "6",
        "options": ["3", "6", "9", "12"]
      }
    }
  }
}
```

Use in templates:
```handlebars
{{#if @custom.show_featured_posts}}
  <section class="featured">
    {{#get "posts" filter="featured:true" limit="3"}}
      {{#foreach posts}}
        <article>{{title}}</article>
      {{/foreach}}
    {{/get}}
  </section>
{{/if}}
```

### Theme Validation with GScan

```bash
# Install GScan
npm install -g gscan

# Validate theme
gscan your-theme-directory

# Validate with specific Ghost version
gscan your-theme-directory --version 5.0

# Output as JSON
gscan your-theme-directory --format json

# Online validation
# Visit https://gscan.ghost.org and upload theme zip
```

Common validation checks:
- Missing required templates (index.hbs, post.hbs)
- Missing required helpers (ghost_head, ghost_foot, body_class)
- Invalid package.json structure
- Deprecated helper usage
- Missing screenshot images
- Incorrect image references

### Dynamic Routing (routes.yaml)

```yaml
routes:
  /about/:
    template: about
  /blog/:
    template: blog

collections:
  /blog/:
    permalink: /blog/{slug}/
    template: blog-post
    filter: tag:blog

taxonomies:
  tag: /tag/{slug}/
  author: /author/{slug}/
```

### Local Development Workflow

```bash
# Start Ghost locally
ghost start

# Access admin at http://localhost:2368/ghost
# Site at http://localhost:2368/

# Development cycle:
# 1. Edit templates in content/themes/your-theme/
# 2. Edit CSS/JS in assets/
# 3. Restart for HBS changes: ghost restart
# 4. CSS/JS changes: instant refresh
# 5. Test at http://localhost:2368/
# 6. Validate with GScan
```

### Publishing Theme

```bash
# Create theme zip (exclude unnecessary files)
cd content/themes/your-theme
zip -r ../your-theme.zip . -x "node_modules/*" ".git/*"

# Upload via Ghost Admin
# Settings > Design > Upload theme
```

## Configuration

### Ghost CLI Configuration

```bash
# Edit Ghost config
ghost config

# Set URL
ghost config url https://your-site.com

# Set mail configuration
ghost config mail {transport, options}

# Restart after config changes
ghost restart
```

### Production Setup (Ubuntu)

```bash
# Full production stack (Nginx, SSL, Systemd)
ghost install

# With custom database
ghost install --db=mysql --dbhost=localhost --dbuser=ghost --dbpass=password --dbname=ghost_prod
```

## Best Practices

### Theme Development

1. **Scope CSS classes** to avoid conflicts with post content
2. **Use semantic HTML** structure throughout templates
3. **Include required helpers** in all templates
4. **Test responsive design** across devices
5. **Optimize images** using Ghost's automatic resizing
6. **Validate frequently** with GScan during development
7. **Keep package.json updated** with correct version and metadata

### Security

1. **Never expose Admin API keys** in client-side code
2. **Use environment variables** for sensitive data
3. **Implement proper authentication** for custom integrations
4. **Keep Ghost updated** with `ghost update`
5. **Validate all inputs** in custom scripts
6. **Use HTTPS** in production

### Performance

1. **Enable image optimization** in theme config
2. **Use appropriate image sizes** for different contexts
3. **Minify CSS/JS** assets
4. **Implement lazy loading** for images
5. **Use CDN** for static assets
6. **Enable Ghost caching**
7. **Optimize database** queries

### API Usage

1. **Use pagination** for large datasets
2. **Filter data** server-side when possible
3. **Include related resources** in single queries when needed
4. **Cache responses** when appropriate
5. **Handle errors gracefully** with try/catch
6. **Use the latest API version**

## Troubleshooting

### Theme Not Loading
```bash
# Check Ghost status
ghost ls

# Restart Ghost
ghost restart

# View logs
ghost log
```

### CSS/JS Not Updating
- Clear browser cache
- Verify file paths in templates
- Check assets are in correct directory
- Restart Ghost if needed

### Template Errors
- Check syntax with GScan
- Verify all required helpers present
- Check for unclosed blocks `{{#if}}...{{/if}}`
- Review Ghost logs for specific errors

### Permission Issues
- Ensure correct file permissions
- Check Ghost is running as correct user
- Verify directory ownership

## Resources

### Comprehensive API Documentation
- **Complete Ghost API Reference**: https://docs.ghost.org/llms-full.txt
  - Full Admin API documentation with all endpoints
  - Authentication methods (Integration tokens, Staff access tokens, User authentication)
  - Token generation examples in multiple languages (Bash, JavaScript, Ruby, Python)
  - Members API (create, update, browse)
  - Newsletters API (create, update, sender email validation)
  - Offers API (create, update, pricing tiers)
  - Pages API management
  - Posts API with card visibility controls
  - Image upload API
  - Admin API JavaScript client usage
  - Complete request/response examples
  - Pagination and filtering guidelines
  - Error handling patterns

### Official Documentation
- Ghost Docs: https://ghost.org/docs/
- Theme Development: https://ghost.org/docs/themes/
- Ghost CLI: https://ghost.org/docs/ghost-cli/
- Content API: https://ghost.org/docs/content-api/
- Admin API: https://ghost.org/docs/admin-api/
- GScan: https://gscan.ghost.org/
- Community Forum: https://forum.ghost.org/
- Ghost GitHub: https://github.com/TryGhost/Ghost

## Categories

web-development, cms, theming, handlebars, blogging, publishing

## Author

Published by Themeix

## License

MIT

## Version

1.0.0
