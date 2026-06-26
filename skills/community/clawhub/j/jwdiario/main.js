#!/usr/bin/env node
/**
 * JWDiario - Texto diario de los Testigos de Jehová en español
 * Obtiene el texto bíblico diario desde wol.jw.org/es/
 */

const { execSync } = require('child_process');

async function main() {
  // Fecha actual
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  
  // URL específica del día en español (¡SIEMPRE en español!)
  const url = `https://wol.jw.org/es/wol/h/r4/lp-s/${year}/${month}/${day}`;
  
  try {
    console.log(`📖 Texto diario - ${day}/${month}/${year}`);
    console.log('');
    
    // Fetch the content using curl
    const html = execSync(`curl -s "${url}"`, { encoding: 'utf-8' });
    
    // Simple parsing with regex (no cheerio needed)
    const todayStr = today.toLocaleDateString('es-ES', { 
      weekday: 'long', 
      day: 'numeric', 
      month: 'long' 
    });
    
    // Find the section for today
    const regex = new RegExp(`##\\s*${todayStr}\\s*\\n([\\s\\S]*?)(?=##\\s*\\d|¡Bienvenido|$)`, 'i');
    const match = html.match(regex);
    
    if (!match || !match[1]) {
      throw new Error('No se encontró el contenido para hoy');
    }
    
    // Extract just the paragraph text (remove HTML tags for cleaner output)
    const content = match[1]
      .replace(/<[^>]+>/g, ' ')  // Remove HTML tags
      .replace(/\s+/g, ' ')       // Normalize whitespace
      .trim();
    
    console.log(content);
    console.log('\n---');
    console.log('📖 [Leer más en wol.jw.org/es/](https://wol.jw.org/es/)');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
