#!/usr/bin/env node

/**
 * HackerNews Skill
 * Monitora e busca stories do HackerNews via API oficial
 */

const axios = require('axios');

const BASE_URL = 'https://hacker-news.firebaseio.com/v0';

// Helper: fetch JSON from HN API
async function fetchHN(endpoint) {
  const response = await axios.get(`${BASE_URL}${endpoint}.json`);
  return response.data;
}

// Get item details
async function getItem(id) {
  return fetchHN(`/item/${id}`);
}

// Get user profile
async function getUser(username) {
  return fetchHN(`/user/${username}`);
}

// Get stories by type
async function getStories(type, limit = 10) {
  const storyIds = await fetchHN(`/${type}stories`);
  const limitedIds = storyIds.slice(0, limit);
  
  const stories = await Promise.all(
    limitedIds.map(id => getItem(id))
  );
  
  return stories;
}

// Format story for output
function formatStory(story, index) {
  const points = story.score || 0;
  const comments = story.descendants || 0;
  const by = story.by || 'unknown';
  const time = new Date(story.time * 1000).toLocaleString('pt-BR');
  
  let url = '';
  if (story.url) {
    try {
      const urlObj = new URL(story.url);
      url = ` (${urlObj.hostname})`;
    } catch {}
  }
  
  return `${index + 1}. ${story.title}${url}
   🔼 ${points} pontos | 💬 ${comments} comentários | por @${by}
   🕐 ${time}
   🔗 https://news.ycombinator.com/item?id=${story.id}`;
}

// Format user profile
function formatUser(user) {
  if (!user) return 'Usuário não encontrado.';
  
  const created = new Date(user.created * 1000).toLocaleString('pt-BR');
  const about = user.about || 'Sem descrição.';
  
  return `👤 @${user.id}
📊 Karma: ${user.karma}
📅 Criado em: ${created}
📝 Sobre: ${about}`;
}

// Search stories by term (filters by title)
async function searchStories(term, limit = 10) {
  // Get recent stories from all categories
  const [top, newest, best] = await Promise.all([
    fetchHN('/topstories'),
    fetchHN('/newstories'),
    fetchHN('/beststories')
  ]);
  
  const allIds = [...new Set([...top, ...newest, ...best])].slice(0, 100);
  
  const stories = await Promise.all(
    allIds.map(id => getItem(id))
  );
  
  const filtered = stories
    .filter(s => s && s.title && s.title.toLowerCase().includes(term.toLowerCase()))
    .slice(0, limit);
  
  return filtered;
}

// Main CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0]?.toLowerCase() || 'top';
  const param = args[1];
  const limit = parseInt(args[2]) || 10;
  
  try {
    switch (command) {
      case 'top':
      case 'frontpage': {
        const stories = await getStories('top', limit);
        console.log(`📰 TOP HACKER NEWS (${stories.length})\n`);
        stories.forEach((s, i) => console.log(formatStory(s, i)));
        break;
      }
      
      case 'new':
      case 'newest':
      case 'latest': {
        const stories = await getStories('new', limit);
        console.log(`🆕 NOVAS HACKER NEWS (${stories.length})\n`);
        stories.forEach((s, i) => console.log(formatStory(s, i)));
        break;
      }
      
      case 'best':
      case 'melhores': {
        const stories = await getStories('best', limit);
        console.log(`⭐ MELHORES HACKER NEWS (${stories.length})\n`);
        stories.forEach((s, i) => console.log(formatStory(s, i)));
        break;
      }
      
      case 'ask': {
        const stories = await getStories('ask', limit);
        console.log(`❓ ASK HN (${stories.length})\n`);
        stories.forEach((s, i) => console.log(formatStory(s, i)));
        break;
      }
      
      case 'show': {
        const stories = await getStories('show', limit);
        console.log(`� SHOW HN (${stories.length})\n`);
        stories.forEach((s, i) => console.log(formatStory(s, i)));
        break;
      }
      
      case 'jobs':
      case 'vagas': {
        const stories = await getStories('job', limit);
        console.log(`💼 JOBS HN (${stories.length})\n`);
        stories.forEach((s, i) => console.log(formatStory(s, i)));
        break;
      }
      
      case 'item': {
        if (!param) {
          console.log('Uso: node index.js item <id>');
          process.exit(1);
        }
        const story = await getItem(param);
        if (!story) {
          console.log('Story não encontrada.');
        } else {
          console.log(formatStory(story, 0));
          if (story.text) {
            console.log(`\n📝 Texto: ${story.text.replace(/<[^>]*>/g, '')}`);
          }
        }
        break;
      }
      
      case 'user': {
        if (!param) {
          console.log('Uso: node index.js user <username>');
          process.exit(1);
        }
        const user = await getUser(param);
        console.log(formatUser(user));
        break;
      }
      
      case 'search':
      case 'buscar': {
        if (!param) {
          console.log('Uso: node index.js search <termo>');
          process.exit(1);
        }
        const term = param === 'search' ? args.slice(2).join(' ') : param;
        const stories = await searchStories(term, limit);
        console.log(`🔍 Resultados para "${term}" (${stories.length})\n`);
        if (stories.length === 0) {
          console.log('Nenhum resultado encontrado.');
        } else {
          stories.forEach((s, i) => console.log(formatStory(s, i)));
        }
        break;
      }
      
      default:
        console.log(`📰 HACKER NEWS
        
Comandos disponíveis:
  top [n]       - Top stories (padrão: 10)
  new [n]       - Stories mais recentes
  best [n]      - Melhores stories
  ask [n]       - Ask HN
  show [n]      - Show HN
  jobs [n]      - Vagas
  item <id>     - Ver detalhes de uma story
  user <nome>   - Ver perfil de usuário
  search <termo> - Buscar stories`);
    }
  } catch (error) {
    console.error('Erro:', error.message);
    process.exit(1);
  }
}

main();
