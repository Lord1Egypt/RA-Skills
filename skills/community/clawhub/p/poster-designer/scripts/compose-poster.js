#!/usr/bin/env node
/**
 * Image Composition Script
 * 
 * Adds text overlays to generated images.
 * Creates composite posters with typography and layout.
 * 
 * Usage:
 *   node compose-poster.js --image ./base.png --title "Event Title" --date "Jan 1" --output ./final.png
 */

const fs = require('fs');
const path = require('path');

// Parse arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    textElements: [],
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    switch (arg) {
      case '--image':
      case '-i':
        options.image = nextArg;
        i++;
        break;
      case '--output':
      case '-o':
        options.output = nextArg;
        i++;
        break;
      case '--title':
      case '-t':
        options.title = nextArg;
        i++;
        break;
      case '--subtitle':
        options.subtitle = nextArg;
        i++;
        break;
      case '--date':
      case '-d':
        options.date = nextArg;
        i++;
        break;
      case '--venue':
      case '-v':
        options.venue = nextArg;
        i++;
        break;
      case '--cta':
        options.cta = nextArg;
        i++;
        break;
      case '--layout':
        options.layout = nextArg; // 'center', 'bottom', 'overlay'
        i++;
        break;
      case '--json':
        options.jsonOutput = true;
        break;
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
        break;
    }
  }

  return options;
}

function showHelp() {
  console.log(`
Image Composition - Add Text to Poster Images

Usage:
  node compose-poster.js --image ./base.png [options]

Options:
  --image, -i        Base image path (required)
  --output, -o       Output path (default: ./composed.png)
  --title, -t        Main title text
  --subtitle         Subtitle/tagline
  --date, -d         Date text
  --venue, -v        Venue/location text
  --cta              Call-to-action text (e.g., "Get Tickets")
  --layout           Text layout: center, bottom, overlay (default: auto)
  --json             Output JSON with text positions
  --help, -h         Show this help

Layouts:
  center     - Text centered over image (good for titles)
  bottom     - Text anchored to bottom (good for event details)
  overlay    - Semi-transparent overlay with text on top

Note: This script requires ImageMagick or Sharp to be installed.
      Without image processing tools, it outputs a metadata JSON
      that can be used with other composition tools.

Example:
  node compose-poster.js --image ./poster.png --title "Summer Fest" --date "July 15" --venue "Central Park"
`);
}

// Calculate text layout positions
function calculateLayout(options) {
  // Default to a balanced layout
  const elements = [];
  
  if (options.title) {
    elements.push({
      type: 'title',
      text: options.title,
      position: options.layout === 'bottom' ? 'bottom-center' : 'top-center',
      size: 'large',
      weight: 'bold',
    });
  }
  
  if (options.subtitle) {
    elements.push({
      type: 'subtitle',
      text: options.subtitle,
      position: options.layout === 'bottom' ? 'bottom-center' : 'top-center',
      size: 'medium',
      weight: 'normal',
    });
  }
  
  if (options.date) {
    elements.push({
      type: 'date',
      text: options.date,
      position: options.layout === 'bottom' ? 'above-bottom' : 'center-left',
      size: 'medium',
      weight: 'normal',
    });
  }
  
  if (options.venue) {
    elements.push({
      type: 'venue',
      text: options.venue,
      position: options.layout === 'bottom' ? 'above-bottom' : 'center-right',
      size: 'medium',
      weight: 'normal',
    });
  }
  
  if (options.cta) {
    elements.push({
      type: 'cta',
      text: options.cta,
      position: 'bottom-center',
      size: 'large',
      weight: 'bold',
      highlight: true,
    });
  }
  
  return elements;
}

// Generate HTML/CSS composition (fallback when no image tools available)
function generateHTMLComposition(imagePath, elements, outputPath) {
  const imageName = path.basename(imagePath);
  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #000;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .poster {
      position: relative;
      max-width: 100%;
      max-height: 100vh;
    }
    .poster img {
      width: 100%;
      height: auto;
      display: block;
    }
    .text-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 40px;
      text-align: center;
      color: white;
      text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .title { 
      font-size: 48px; 
      font-weight: bold; 
      margin-bottom: 10px;
      letter-spacing: -1px;
    }
    .subtitle { 
      font-size: 24px; 
      opacity: 0.9; 
    }
    .details {
      display: flex;
      justify-content: center;
      gap: 40px;
      font-size: 20px;
    }
    .cta {
      background: rgba(255,255,255,0.9);
      color: #000;
      padding: 15px 40px;
      border-radius: 30px;
      font-size: 18px;
      font-weight: bold;
      display: inline-block;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="poster">
    <img src="${imageName}" alt="Poster background">
    <div class="text-overlay">
      <div class="top-section">
        ${elements.filter(e => e.position.includes('top')).map(e => 
          `<div class="${e.type}">${e.text}</div>`
        ).join('')}
      </div>
      <div class="middle-section">
        ${elements.filter(e => e.position.includes('center')).map(e => 
          `<div class="${e.type}">${e.text}</div>`
        ).join('')}
      </div>
      <div class="bottom-section">
        <div class="details">
          ${elements.filter(e => e.position.includes('bottom') || e.position.includes('above-bottom')).map(e => 
            e.type === 'cta' 
              ? `<div class="${e.type}">${e.text}</div>`
              : `<span class="${e.type}">${e.text}</span>`
          ).join('')}
        </div>
      </div>
    </div>
  </div>
</body>
</html>`;

  const htmlPath = outputPath.replace(/\.[^/.]+$/, '') + '.html';
  fs.writeFileSync(htmlPath, html);
  return htmlPath;
}

// Generate ImageMagick command
function generateImageMagickCommand(imagePath, elements, outputPath) {
  // Build ImageMagick convert command
  let cmd = `convert "${imagePath}"`;
  
  // Add text elements
  elements.forEach((el, idx) => {
    const fontSize = el.size === 'large' ? 48 : el.size === 'medium' ? 32 : 24;
    const fontWeight = el.weight === 'bold' ? 'bold' : 'normal';
    
    // Calculate position (simplified)
    let x = 50; // percentage
    let y = 10 + idx * 15; // percentage
    
    if (el.position.includes('center')) x = 50;
    if (el.position.includes('bottom')) y = 80 + idx * 10;
    if (el.position.includes('left')) x = 25;
    if (el.position.includes('right')) x = 75;
    
    cmd += ` \\\n      -gravity center \\\n      -fill white \\\n      -stroke black \\\n      -strokewidth 2 \\\n      -pointsize ${fontSize} \\\n      -annotate +0+${(idx - 2) * 60} "${el.text.replace(/"/g, '\\"')}"`;
  });
  
  cmd += ` "${outputPath}"`;
  
  return cmd;
}

// Main function
async function main() {
  try {
    const options = parseArgs();
    
    if (!options.image) {
      throw new Error('Image path required. Use --image or -i');
    }
    
    if (!fs.existsSync(options.image)) {
      throw new Error(`Image not found: ${options.image}`);
    }
    
    // Calculate layout
    const elements = calculateLayout(options);
    
    if (elements.length === 0) {
      throw new Error('No text elements provided. Use --title, --date, --venue, etc.');
    }
    
    const outputPath = path.resolve(options.output || './composed.png');
    
    // Check for ImageMagick
    const { execSync } = require('child_process');
    let hasImageMagick = false;
    try {
      execSync('which convert', { stdio: 'ignore' });
      hasImageMagick = true;
    } catch {}
    
    let result = {
      baseImage: path.resolve(options.image),
      elements: elements,
      outputPath: outputPath,
    };
    
    if (hasImageMagick) {
      // Use ImageMagick
      const cmd = generateImageMagickCommand(options.image, elements, outputPath);
      console.error('Running ImageMagick composition...');
      execSync(cmd, { stdio: 'inherit' });
      result.composed = true;
      result.method = 'imagemagick';
    } else {
      // Generate HTML composition as fallback
      console.error('ImageMagick not found, generating HTML composition...');
      const htmlPath = generateHTMLComposition(options.image, elements, outputPath);
      result.htmlPath = htmlPath;
      result.method = 'html';
      result.note = 'Open the HTML file in a browser and screenshot for final image';
    }
    
    if (options.jsonOutput) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.error(`\n✓ Composition created`);
      console.error(`  Base image: ${result.baseImage}`);
      if (result.htmlPath) {
        console.error(`  HTML file: ${result.htmlPath}`);
        console.error(`  Note: ${result.note}`);
      } else {
        console.error(`  Output: ${result.outputPath}`);
      }
      console.error(`  Elements: ${elements.length}`);
      elements.forEach(e => {
        console.error(`    - ${e.type}: "${e.text}" (${e.position})`);
      });
    }
    
  } catch (err) {
    console.error(`\n✗ Error: ${err.message}`);
    process.exit(1);
  }
}

main();
