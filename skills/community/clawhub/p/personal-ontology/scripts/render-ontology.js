#!/usr/bin/env node
/**
 * Render Personal Ontology as Mermaid diagram
 * 
 * Usage: node render-ontology.js [--ascii] [--svg output.svg]
 * 
 * Reads ontology files from the configured location and generates
 * a Mermaid graph visualization.
 */

const fs = require('fs');
const path = require('path');

// Default ontology location - customize via ONTOLOGY_DIR env var
const ONTOLOGY_DIR = process.env.ONTOLOGY_DIR || 
  path.join(process.cwd(), 'My_Personal_Ontology');

// Parse ontology files and extract objects + links
function parseOntologyFiles() {
  const objects = [];
  const links = [];
  
  const files = [
    '1-higher-order.md',
    '2-beliefs.md', 
    '3-predictions.md',
    '4-core-self.md',
    '5-goals.md',
    '6-projects.md'
  ];
  
  for (const file of files) {
    const filePath = path.join(ONTOLOGY_DIR, file);
    if (!fs.existsSync(filePath)) continue;
    
    const content = fs.readFileSync(filePath, 'utf-8');
    const type = file.replace(/^\d+-/, '').replace('.md', '');
    
    // Extract objects (## headers with IDs)
    const objectRegex = /^## ([A-Z0-9]+) — (.+)$/gm;
    let match;
    while ((match = objectRegex.exec(content)) !== null) {
      objects.push({
        id: match[1],
        name: match[2].substring(0, 30) + (match[2].length > 30 ? '...' : ''),
        type: type
      });
    }
    
    // Extract links from ### Links sections
    const linkRegex = /`(serves|supports|contradicts|relates-to|depends-on|served-by|supported-by)`\s*→\s*(?:\[\[#)?([A-Z0-9]+)?/gm;
    let currentObject = null;
    const lines = content.split('\n');
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const objMatch = line.match(/^## ([A-Z0-9]+) — /);
      if (objMatch) {
        currentObject = objMatch[1];
      }
      
      if (currentObject) {
        const linkMatch = line.match(/`(serves|supports|contradicts|relates-to|depends-on|served-by|supported-by)`\s*→\s*(?:\[\[#)?([A-Z0-9]+)?/);
        if (linkMatch) {
          const linkType = linkMatch[1];
          const target = linkMatch[2];
          if (target) {
            // Normalize link direction
            if (linkType === 'served-by' || linkType === 'supported-by') {
              links.push({ from: target, to: currentObject, type: linkType.replace('-by', '') });
            } else {
              links.push({ from: currentObject, to: target, type: linkType });
            }
          }
        }
      }
    }
  }
  
  // Add Core Self as a special node
  objects.push({ id: 'CORE', name: 'Core Self (Mission)', type: 'core-self' });
  
  return { objects, links };
}

// Generate Mermaid syntax
function generateMermaid(objects, links) {
  const lines = ['graph TD'];
  
  // Define node styles by type
  const typeStyles = {
    'higher-order': ':::higherOrder',
    'beliefs': ':::belief',
    'predictions': ':::prediction',
    'core-self': ':::coreSelf',
    'goals': ':::goal',
    'projects': ':::project'
  };
  
  // Add subgraphs by type
  const byType = {};
  for (const obj of objects) {
    if (!byType[obj.type]) byType[obj.type] = [];
    byType[obj.type].push(obj);
  }
  
  // Add nodes
  for (const obj of objects) {
    const shape = obj.type === 'core-self' ? `((${obj.name}))` : `[${obj.name}]`;
    lines.push(`    ${obj.id}${shape}`);
  }
  
  lines.push('');
  
  // Add links
  for (const link of links) {
    const arrow = link.type === 'contradicts' ? '-.->|contradicts|' : 
                  link.type === 'supports' ? '-->|supports|' :
                  link.type === 'serves' ? '-->|serves|' :
                  '-->';
    lines.push(`    ${link.from} ${arrow} ${link.to}`);
  }
  
  // Add style definitions
  lines.push('');
  lines.push('    classDef coreSelf fill:#f9f,stroke:#333,stroke-width:2px');
  lines.push('    classDef belief fill:#bbf,stroke:#333');
  lines.push('    classDef goal fill:#bfb,stroke:#333');
  lines.push('    classDef project fill:#fbb,stroke:#333');
  
  return lines.join('\n');
}

// Main execution
async function main() {
  const args = process.argv.slice(2);
  const useAscii = args.includes('--ascii');
  const svgIndex = args.indexOf('--svg');
  const svgOutput = svgIndex !== -1 ? args[svgIndex + 1] : null;
  
  const { objects, links } = parseOntologyFiles();
  const mermaidCode = generateMermaid(objects, links);
  
  if (useAscii) {
    try {
      const { renderMermaidAscii } = require('beautiful-mermaid');
      const ascii = renderMermaidAscii(mermaidCode);
      console.log(ascii);
    } catch (e) {
      console.log('ASCII rendering requires beautiful-mermaid');
      console.log('\nMermaid code:\n');
      console.log(mermaidCode);
    }
  } else if (svgOutput) {
    try {
      const { renderMermaid, THEMES } = require('beautiful-mermaid');
      const svg = await renderMermaid(mermaidCode, THEMES['tokyo-night']);
      fs.writeFileSync(svgOutput, svg);
      console.log(`SVG written to ${svgOutput}`);
    } catch (e) {
      console.error('SVG rendering failed:', e.message);
      console.log('\nMermaid code:\n');
      console.log(mermaidCode);
    }
  } else {
    // Just output the Mermaid code
    console.log(mermaidCode);
  }
}

main().catch(console.error);
