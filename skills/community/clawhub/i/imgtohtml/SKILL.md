---
name: img2html
description: "Convert UI screenshots/images into fully functional HTML/CSS copies. This skill is used when a user provides images of a website, application interface, dashboard, or any UI design and wants to recreate it as working HTML code with accurate styles, layout, and visual details."
license: Complete terms in LICENSE.txt
---

This skill converts UI screenshots or design images into production-ready HTML/CSS code that accurately replicates the visual appearance and layout of the original.

The user provides an image (screenshot, mockup, or design reference) showing a UI interface they want replicated.

## Analysis Process

First, carefully analyze the image to understand:

1. **Layout Structure**
   
   - Identify sections, containers, and nesting hierarchy
   - Determine grid/flexbox patterns needed
   - Note spacing relationships and alignment

2. **Visual Elements**
   
   - Colors (hex/rgb values from the image)
   - Typography (font families, sizes, weights)
   - Icons and imagery
   - Borders, shadows, gradients, effects

3. **Component Types**
   
   - Headers, navigation, cards, buttons, inputs, tables, etc.
   - Interactive elements and their states
   - Data displays, labels, badges

4. **Responsive Behavior**
   
   - How the layout might adapt to different screen sizes
   - Mobile-first or desktop-first approach

## Implementation Guidelines

**HTML Structure:**

- Use semantic HTML5 elements (header, nav, main, section, article, footer)
- Create logical nesting that matches the visual hierarchy
- Use meaningful class names (BEM or similar convention)

**CSS Styling:**

- Replicate colors exactly using values from the image
- Match typography (font family, size, weight, line-height, letter-spacing)
- Recreate spacing (margins, padding, gaps) accurately
- Implement visual effects (box-shadow, border-radius, gradients, backdrop-filter)
- Use CSS variables for theming when appropriate

**Layout Techniques:**

- Flexbox for 1D layouts (rows or columns)
- CSS Grid for 2D layouts
- Position properties for overlays and absolute positioning
- Transform for rotations and scaling

**Interactive Elements:**

- Add :hover, :focus states for buttons and links
- Include transitions for smooth state changes
- Consider adding basic JavaScript if the UI implies interactivity

## Output Format

Provide a complete, self-contained HTML file with:

- Proper DOCTYPE and HTML structure
- Embedded CSS in `<style>` tags (or separate CSS file if complex)
- All necessary meta tags for viewport/responsiveness
- Comments explaining major sections if helpful

If the design is complex, you may split into multiple files (HTML, CSS, JS).

## Accuracy Priorities

1. **Visual Fidelity**: Match the original image as closely as possible
2. **Proportions**: Maintain correct size ratios between elements
3. **Colors**: Use exact or nearest-match color values
4. **Typography**: Match font styles accurately
5. **Spacing**: Replicate padding, margins, and gaps faithfully

## Limitations to Communicate

- Exact font matching may require web fonts (Google Fonts, etc.)
- Some effects may be approximated if the exact technique isn't visible
- Interactive behavior beyond hover states requires user specification
- Dynamic content should be represented with placeholder data

## Multi-Image Handling

When the user provides multiple images at once, process each image **individually and sequentially** to ensure maximum quality:

**Sequential Processing Workflow:**

1. Process ONE image at a time through the complete conversion pipeline
2. For each image:
   - Analyze its unique layout, colors, typography, and components
   - Create a dedicated HTML/CSS replica
   - Verify visual fidelity before moving to the next
3. Maintain consistent naming conventions across all generated files
4. After processing all images, provide a summary of all converted files

**Output Organization:**

- Name files descriptively based on each image's content (e.g., `login-page.html`, `dashboard.html`)
- If images represent different pages of the same site, maintain shared styles in a common CSS file when appropriate
- If images are unrelated, create self-contained HTML files for each

**Quality Assurance:**

- Do NOT batch-process images together - each deserves full analysis attention
- If images are related (e.g., different screens of the same app), note shared components and reuse CSS where sensible
- Communicate progress to the user as you work through each image

## Example Workflow

1. User provides UI screenshot(s)
2. For each image:
   - Analyze layout, colors, typography, components
   - Create HTML structure matching the hierarchy
   - Apply CSS to replicate visual appearance
   - Add polish (hover states, transitions, responsive considerations)
3. Deliver complete HTML file(s) - one per input image (or split logically for multi-page designs)

Remember: The goal is a pixel-perfect replica that functions as a real web page, not just a close approximation. Pay attention to details like shadows, borders, gradients, and spacing - these make the difference between "close" and "indistinguishable."
