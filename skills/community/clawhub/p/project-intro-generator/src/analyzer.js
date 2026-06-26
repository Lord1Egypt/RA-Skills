const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const { pathExists, readTextFile, detectLanguage, formatBytes, isTextFile } = require('./utils');

marked.setOptions({ mangle: false, headerIds: true, breaks: false });

const README_CANDIDATES = ['README.md', 'Readme.md', 'readme.md', 'README', 'readme'];
const IGNORE_DIRS = new Set([
  'node_modules', '.git', '.hg', '.svn', '.DS_Store', 'dist', 'build', 'out', '.next', '.nuxt',
  '.turbo', '.vercel', '.cache', 'coverage', 'logs', '.idea', '.vscode', '.trae'
]);

const BACKEND_FRAMEWORKS = ['express', 'koa', 'nestjs', 'fastify', '@hapi/hapi', 'hapi', 'egg', 'sails', 'adonis', 'strapi', 'laravel', 'symfony', 'spring-boot', 'gin', 'echo', 'fastapi', 'django', 'flask', 'sanic', 'pyramid', 'actix', 'axum', 'warp'];
const FRONTEND_FRAMEWORKS = ['react', 'next', 'nextjs', 'remix', 'vue', 'nuxt', 'nuxt3', '@nuxtjs', 'vite', 'angular', '@angular/core', 'svelte', 'sveltekit', 'astro', 'gatsby', 'solid', 'preact'];
const API_DOC_HINTS = ['docs/api', 'api-docs', 'openapi', 'swagger', 'spec', 'postman'];

const PACKAGE_MANAGERS = [
  { file: 'Cargo.toml', name: 'Rust (Cargo)' },
  { file: 'go.mod', name: 'Go' },
  { file: 'requirements.txt', name: 'Python (pip)' },
  { file: 'pyproject.toml', name: 'Python (Poetry)' },
  { file: 'pom.xml', name: 'Java (Maven)' },
  { file: 'build.gradle', name: 'Java/Android (Gradle)' },
  { file: 'Gemfile', name: 'Ruby' },
  { file: 'composer.json', name: 'PHP' },
  { file: 'Podfile', name: 'iOS (CocoaPods)' },
  { file: 'Package.swift', name: 'Swift (SPM)' },
  { file: 'project.clj', name: 'Clojure' },
  { file: 'mix.exs', name: 'Elixir' },
  { file: 'shard.yml', name: 'Crystal' }
];

const FRONTEND_TECHS = {
  frameworks: ['react', 'vue', 'angular', 'svelte', 'solid', 'preact'],
  ssr: ['next', 'nextjs', 'nuxt', 'nuxtjs', 'nuxt3', 'svelte-kit', 'sveltekit', 'gatsby', 'astro', 'remix'],
  build: ['vite', 'webpack', 'rollup', 'esbuild', 'parcel', 'snowpack'],
  styling: ['tailwindcss', 'tailwind', 'sass', 'scss', 'less', 'styled-components', 'emotion', 'postcss', 'bootstrap'],
  state: ['redux', 'zustand', 'jotai', 'recoil', 'vuex', 'pinia', 'mobx'],
  routing: ['react-router', 'vue-router', 'wouter', 'tanstack-router'],
  ui: ['antd', 'element-ui', 'element-plus', 'material-ui', 'mui', 'chakra-ui', 'shadcn', 'headlessui', 'radix-ui', 'bootstrap', 'mantine'],
  http: ['axios', 'fetch', 'ky', 'react-query', 'swr', 'apollo', 'urql'],
  testing: ['jest', 'vitest', 'cypress', 'playwright', 'testing-library', 'mocha']
};

const BACKEND_TECHS = {
  node: ['express', 'fastify', 'koa', 'nest', 'hapi', 'sails', 'adonis', 'strapi', 'mongoose', 'typeorm', 'prisma', 'sequelize', 'passport', 'jsonwebtoken', 'socket.io', 'bull', 'winston', 'pino', 'bunyan'],
  python: ['django', 'flask', 'fastapi', 'bottle', 'tornado', 'sanic', 'pyramid', 'sqlalchemy', 'peewee', 'djangorestframework', 'celery'],
  java: ['spring-boot', 'spring-web', 'spring-cloud', 'jfinal', 'javalin', 'mybatis', 'mybatis-plus', 'hibernate', 'lombok', 'hutool', 'guava', 'dubbo'],
  go: ['gin', 'echo', 'fiber', 'beego', 'chi', 'gorm', 'sqlx', 'grpc', 'kratos', 'viper', 'zap', 'logrus', 'iris'],
  php: ['laravel', 'symfony', 'thinkphp', 'yii', 'slim', 'eloquent', 'doctrine', 'blade', 'twig'],
  rust: ['actix-web', 'axum', 'warp', 'rocket', 'tide', 'diesel', 'sqlx', 'tokio', 'reqwest'],
  dotnet: ['aspnetcore', 'asp.net', 'entity-framework', 'dapper', 'serilog', 'nlog']
};

const BUSINESS_KEYWORDS = {
  '金融/区块链': ['trading', 'exchange', 'wallet', 'crypto', 'blockchain'],
  '爬虫': ['crawler', 'spider', 'scraper'],
  '管理后台': ['admin', 'dashboard', 'panel', 'management'],
  '网关/代理': ['gateway', 'proxy'],
  '任务队列': ['worker', 'task', 'queue', 'job'],
  '即时通讯': ['chat', 'im', 'message', 'messenger'],
  '支付/计费': ['payment', 'billing', 'pay'],
  '电商': ['order', 'cart', 'shop', 'mall', 'store', 'commerce'],
  '内容管理': ['cms', 'content', 'article'],
  '博客': ['blog'],
  '社区': ['forum', 'community'],
  '办公自动化': ['oa', 'office'],
  '企业资源计划': ['erp'],
  '客户关系管理': ['crm'],
  '学习管理': ['lms', 'learning', 'edu'],
  '库存管理': ['inventory', 'stock', 'warehouse'],
  '预约系统': ['booking', 'reservation', 'appointment'],
  '数据分析': ['analytics', 'report', 'bi'],
  'AI/机器学习': ['ai', 'ml', 'model', 'deeplearning', 'pytorch', 'tensorflow'],
  '物联网': ['iot', 'sensor', 'device']
};

function isMeaningfulReadme(content) {
  if (!content) return false;
  const words = content.split(/\s+/).filter(Boolean).length;
  const lines = content.split(/\r?\n/).filter(Boolean).length;
  return words >= 30 || lines >= 5;
}

async function loadReadme(projectPath) {
  for (const candidate of README_CANDIDATES) {
    const filePath = path.join(projectPath, candidate);
    if (await pathExists(filePath)) {
      const content = await readTextFile(filePath);
      return { filePath, content };
    }
  }
  return null;
}

async function loadPackageJson(projectPath) {
  const pkgPath = path.join(projectPath, 'package.json');
  if (!(await pathExists(pkgPath))) return null;
  try {
    const json = JSON.parse(await readTextFile(pkgPath));
    return { pkgPath, json };
  } catch (err) {
    return null;
  }
}

async function scanProject(projectPath, options = {}) {
  const { maxFiles = 1200 } = options;
  const stack = [projectPath];
  const languages = new Map();
  const keyFiles = [];
  const topDirs = new Map();
  const controllers = [];
  const services = [];
  const routes = [];
  const components = [];
  const pages = [];
  const htmlFiles = [];
  const apiDocs = [];
  const entryFiles = [];
  let totalFiles = 0;

  while (stack.length > 0 && totalFiles < maxFiles) {
    const current = stack.pop();
    const entries = await fs.promises.readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name.startsWith('.DS_Store')) continue;
      const fullPath = path.join(current, entry.name);
      const relative = path.relative(projectPath, fullPath);

      if (entry.isDirectory()) {
        if (IGNORE_DIRS.has(entry.name)) continue;
        if (!relative) continue;
        const top = relative.split(path.sep)[0];
        if (top) {
          topDirs.set(top, (topDirs.get(top) || 0) + 1);
        }
        stack.push(fullPath);
      } else {
        totalFiles += 1;
        const ext = path.extname(entry.name);
        const lang = detectLanguage(ext);
        if (lang) {
          languages.set(lang, (languages.get(lang) || 0) + 1);
        }

        try {
          const stat = await fs.promises.stat(fullPath);
          keyFiles.push({ path: relative, size: stat.size, sizeLabel: formatBytes(stat.size) });
        } catch (err) {}

        const lower = relative.toLowerCase();
        if (ext === '.html') {
          htmlFiles.push(relative);
        }
        if (/\bcontroller\b/.test(lower)) {
          controllers.push(relative);
        }
        if (/\bservice\b/.test(lower)) {
          services.push(relative);
        }
        if (/\broutes?\b/.test(lower)) {
          routes.push(relative);
        }
        if (lower.includes(`components${path.sep}`) || lower.includes('component')) {
          if (['.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte'].includes(ext)) {
            components.push(relative);
          }
        }
        if (lower.includes(`pages${path.sep}`) || lower.includes(`app${path.sep}`)) {
          if (['.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte'].includes(ext)) {
            pages.push(relative);
          }
        }
        if (API_DOC_HINTS.some((hint) => lower.includes(hint))) {
          apiDocs.push(relative);
        }

        const entryNames = ['index.html', 'main.js', 'main.ts', 'main.tsx', 'main.py', 'main.go', 'main.java', 'app.js', 'server.js', 'App.jsx'];
        if (entryNames.includes(entry.name)) {
          entryFiles.push(relative);
        }
      }
      if (totalFiles >= maxFiles) break;
    }
  }

  keyFiles.sort((a, b) => b.size - a.size);
  return {
    totalFiles,
    languages: Array.from(languages.entries()).map(([name, count]) => ({ name, count })),
    keyFiles: keyFiles.slice(0, 8),
    topDirs: Array.from(topDirs.entries()).map(([name, count]) => ({ name, count })),
    controllers: controllers.slice(0, 10),
    services: services.slice(0, 10),
    routes: routes.slice(0, 10),
    components: components.slice(0, 12),
    pages: pages.slice(0, 12),
    htmlFiles: htmlFiles.slice(0, 6),
    apiDocs: apiDocs.slice(0, 12),
    entryFiles: entryFiles.slice(0, 10)
  };
}

function firstMeaningfulLine(content) {
  if (!content) return '';
  const lines = content.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  return lines.find((line) => line.length > 8) || lines[0] || '';
}

function detectProjectType(stats, pkgJson) {
  const dirs = new Set(stats.topDirs.map(d => d.name));
  const entryFiles = new Set(stats.entryFiles || []);
  const deps = pkgJson ? { ...pkgJson.dependencies, ...pkgJson.devDependencies } : {};
  const depNames = Object.keys(deps).map(k => k.toLowerCase());

  const has = (d) => dirs.has(d);
  const hasEntry = (name) => entryFiles.has(name) || stats.keyFiles.some(f => f.path.includes(name));
  const hasDep = (pattern) => depNames.some(d => d.includes(pattern));

  const isFrontend = (
    has('public') ||
    (has('src') && stats.htmlFiles.length > 0) ||
    stats.htmlFiles.some(f => f.includes('index.html')) ||
    has('components') ||
    has('pages') ||
    hasEntry('vite.config') ||
    hasEntry('webpack.config') ||
    hasDep('vite') ||
    hasDep('webpack') ||
    hasDep('rollup') ||
    hasDep('esbuild')
  );

  const isBackend = (
    has('routes') ||
    has('controllers') ||
    has('services') ||
    has('models') ||
    hasEntry('app.js') ||
    hasEntry('server.js') ||
    hasEntry('main.go') ||
    hasEntry('main.py') ||
    hasEntry('main.java') ||
    hasDep('express') ||
    hasDep('koa') ||
    hasDep('nest') ||
    hasDep('fastify') ||
    hasDep('django') ||
    hasDep('flask') ||
    hasDep('fastapi') ||
    hasDep('spring-boot') ||
    hasDep('gin') ||
    hasDep('echo')
  );

  const isFullstack = (
    (has('client') && has('server')) ||
    has('api') ||
    (isFrontend && isBackend)
  );

  const isMobile = (
    (has('android') && has('ios')) ||
    (has('lib') && has('pubspec.yaml')) ||
    hasDep('react-native') ||
    hasDep('flutter')
  );

  const isDesktop = (
    (has('main') && has('renderer')) ||
    hasEntry('electron-builder.json') ||
    hasDep('electron')
  );

  const isDataScience = (
    has('notebooks') ||
    has('data') ||
    has('models') ||
    hasDep('pandas') ||
    hasDep('numpy') ||
    hasDep('tensorflow') ||
    hasDep('pytorch') ||
    hasDep('scikit-learn')
  );

  const isDevOps = (
    has('terraform') ||
    has('ansible') ||
    has('kubernetes') ||
    has('.github') ||
    hasEntry('Jenkinsfile') ||
    hasEntry('docker-compose')
  );

  const isTool = (
    has('bin') ||
    has('__tests__') ||
    has('benchmark') ||
    has('tests')
  );

  if (isFullstack) return { kind: 'fullstack', type: 'fullstack' };
  if (isDevOps) return { kind: 'devops', type: 'devops' };
  if (isMobile) return { kind: 'mobile', type: 'mobile' };
  if (isDesktop) return { kind: 'desktop', type: 'desktop' };
  if (isDataScience) return { kind: 'data-science', type: 'data-science' };
  if (isTool) return { kind: 'tool', type: 'tool' };
  if (isFrontend) return { kind: 'frontend', type: 'frontend' };
  if (isBackend) return { kind: 'backend', type: 'backend' };

  return { kind: 'unknown', type: 'unknown' };
}

function detectTechStack(pkgJson) {
  const deps = pkgJson ? { ...pkgJson.dependencies, ...pkgJson.devDependencies } : {};
  const depNames = Object.keys(deps).map(k => k.toLowerCase());

  const detected = { frontend: [], backend: [], mobile: [], desktop: [], dataScience: [] };

  for (const list of Object.values(FRONTEND_TECHS)) {
    for (const tech of list) {
      if (depNames.some(d => d.includes(tech))) {
        detected.frontend.push(tech);
      }
    }
  }

  for (const list of Object.values(BACKEND_TECHS)) {
    for (const tech of list) {
      if (depNames.some(d => d.includes(tech))) {
        detected.backend.push(tech);
      }
    }
  }

  if (depNames.some(d => d.includes('react-native'))) detected.mobile.push('React Native');
  if (depNames.some(d => d.includes('flutter'))) detected.mobile.push('Flutter');
  if (depNames.some(d => d.includes('electron'))) detected.desktop.push('Electron');

  if (depNames.some(d => d.includes('tensorflow') || d.includes('pytorch') || d.includes('scikit'))) {
    detected.dataScience.push('ML/AI');
  }
  if (depNames.some(d => d.includes('pandas') || d.includes('numpy'))) {
    detected.dataScience.push('Data Processing');
  }

  return detected;
}

function detectBusinessScenario(stats) {
  const allPaths = [
    ...stats.controllers,
    ...stats.services,
    ...stats.routes,
    ...stats.components,
    ...stats.pages,
    ...stats.topDirs.map(d => d.name)
  ].map(p => p.toLowerCase());

  const scenarios = [];
  for (const [scenario, keywords] of Object.entries(BUSINESS_KEYWORDS)) {
    if (keywords.some(kw => allPaths.some(p => p.includes(kw)))) {
      scenarios.push(scenario);
    }
  }

  return scenarios.slice(0, 3);
}

function detectProfile(pkgJson, stats, githubInfo = null) {
  const frameworks = new Set();
  const deps = pkgJson ? { ...pkgJson.dependencies, ...pkgJson.devDependencies } : {};
  const depNames = Object.keys(deps || {});
  depNames.forEach((name) => {
    const lower = name.toLowerCase();
    if (BACKEND_FRAMEWORKS.some((f) => lower.includes(f))) frameworks.add(name);
    if (FRONTEND_FRAMEWORKS.some((f) => lower.includes(f))) frameworks.add(name);
  });

  const typeInfo = { kind: 'unknown', language: null, source: 'local' };
  const projectType = detectProjectType(stats, pkgJson);

  let kind = typeInfo.kind;
  if (kind === 'unknown' && projectType.kind !== 'unknown') {
    kind = projectType.kind;
  }
  if (kind === 'unknown') {
    const hasBackend = stats.controllers.length > 0 || stats.services.length > 0 || stats.routes.length > 0;
    const hasFrontend = stats.components.length > 0 || stats.pages.length > 0 || stats.htmlFiles.length > 0;
    if (hasFrontend && hasBackend) kind = 'fullstack';
    else if (hasBackend) kind = 'backend';
    else if (hasFrontend) kind = 'frontend';
  }

  const techStack = detectTechStack(pkgJson);
  const businessScenarios = detectBusinessScenario(stats);

  return {
    kind,
    projectType: projectType.type,
    frameworks: Array.from(frameworks).slice(0, 8),
    language: typeInfo.language,
    languageSource: typeInfo.source,
    githubInfo,
    techStack,
    businessScenarios,
    backend: {
      controllers: stats.controllers,
      services: stats.services,
      routes: stats.routes,
      apiDocs: stats.apiDocs
    },
    frontend: {
      components: stats.components,
      pages: stats.pages,
      htmlFiles: stats.htmlFiles
    }
  };
}

async function extractCoreNotes(projectPath, keyFiles) {
  const notes = [];
  const candidates = (keyFiles || [])
    .filter(f => {
      const lower = f.path.toLowerCase();
      if (lower.includes('public/') || lower.includes('assets/') || lower.includes('apidoc') || lower.includes('.min.')) return false;
      const ext = path.extname(lower);
      const allowed = ['.js', '.jsx', '.ts', '.tsx', '.py', '.go', '.java', '.rs', '.rb', '.php', '.cs', '.cpp', '.c', '.json', '.yml', '.yaml', '.md'];
      if (!allowed.includes(ext)) return false;
      return true;
    })
    .slice(0, 8);

  for (const file of candidates) {
    const fullPath = path.join(projectPath, file.path);
    try {
      const stat = await fs.promises.stat(fullPath);
      if (stat.size > 512 * 1024) continue;
    } catch (e) {
      continue;
    }
    if (!isTextFile(path.extname(fullPath))) continue;
    try {
      const content = await readTextFile(fullPath);
      const short = content.slice(0, 4000);
      const lines = short.split(/\r?\n/);
      const commentLines = lines
        .filter((line) => /^\s*(\/\/|#|<!--|\*|\/\*)/.test(line))
        .map((l) => l.trim())
        .slice(0, 5);
      if (commentLines.length > 0) {
        notes.push({ path: file.path, comments: commentLines });
      }
    } catch (err) {}
    if (notes.length >= 3) break;
  }
  return notes;
}

async function detectPackageManagerFile(projectPath) {
  for (const pm of PACKAGE_MANAGERS) {
    if (await pathExists(path.join(projectPath, pm.file))) {
      return pm.name;
    }
  }
  return null;
}

function toDepMap(pairs) {
  return pairs.reduce((acc, [name, version]) => {
    if (!name) return acc;
    acc[name] = version || '';
    return acc;
  }, {});
}

async function parsePackageJson(projectPath) {
  const pkgPath = path.join(projectPath, 'package.json');
  if (!(await pathExists(pkgPath))) return null;
  try {
    const json = JSON.parse(await readTextFile(pkgPath));
    return {
      manager: 'npm',
      label: 'Node (package.json)',
      dependencies: json.dependencies || {},
      devDependencies: json.devDependencies || {},
      source: pkgPath
    };
  } catch (e) {
    return null;
  }
}

async function parseRequirements(projectPath) {
  const reqPath = path.join(projectPath, 'requirements.txt');
  if (!(await pathExists(reqPath))) return null;
  const lines = (await readTextFile(reqPath)).split(/\r?\n/);
  const pairs = lines
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#'))
    .map((l) => {
      const parts = l.split('==');
      return [parts[0].trim(), parts[1] ? parts[1].trim() : ''];
    });
  return {
    manager: 'pip',
    label: 'Python (requirements.txt)',
    dependencies: toDepMap(pairs),
    devDependencies: {},
    source: reqPath
  };
}

async function parseGoMod(projectPath) {
  const modPath = path.join(projectPath, 'go.mod');
  if (!(await pathExists(modPath))) return null;
  const lines = (await readTextFile(modPath)).split(/\r?\n/);
  const pairs = [];
  let inBlock = false;
  for (const line of lines) {
    const l = line.trim();
    if (l.startsWith('require (')) { inBlock = true; continue; }
    if (inBlock && l === ')') { inBlock = false; continue; }
    if (l.startsWith('require')) {
      const parts = l.replace('require', '').trim().split(/\s+/);
      if (parts[0]) pairs.push([parts[0], parts[1] || '']);
      continue;
    }
    if (inBlock && l) {
      const parts = l.split(/\s+/);
      if (parts[0]) pairs.push([parts[0], parts[1] || '']);
    }
  }
  return {
    manager: 'go',
    label: 'Go (go.mod)',
    dependencies: toDepMap(pairs),
    devDependencies: {},
    source: modPath
  };
}

async function parseCargoToml(projectPath) {
  const cargoPath = path.join(projectPath, 'Cargo.toml');
  if (!(await pathExists(cargoPath))) return null;
  const lines = (await readTextFile(cargoPath)).split(/\r?\n/);
  const pairs = [];
  let inDeps = false;
  for (const line of lines) {
    const l = line.trim();
    if (l.startsWith('[dependencies]')) { inDeps = true; continue; }
    if (l.startsWith('[') && !l.startsWith('[dependencies]')) { inDeps = false; }
    if (!inDeps || !l || l.startsWith('#')) continue;
    const eq = l.split('=');
    if (eq.length >= 2) {
      const name = eq[0].trim();
      const ver = eq.slice(1).join('=').replace(/"/g, '').trim();
      pairs.push([name, ver]);
    }
  }
  return {
    manager: 'cargo',
    label: 'Rust (Cargo.toml)',
    dependencies: toDepMap(pairs),
    devDependencies: {},
    source: cargoPath
  };
}

async function parseComposer(projectPath) {
  const compPath = path.join(projectPath, 'composer.json');
  if (!(await pathExists(compPath))) return null;
  try {
    const json = JSON.parse(await readTextFile(compPath));
    return {
      manager: 'composer',
      label: 'PHP (composer.json)',
      dependencies: json.require || {},
      devDependencies: json['require-dev'] || {},
      source: compPath
    };
  } catch (e) {
    return null;
  }
}

async function parsePom(projectPath) {
  const pomPath = path.join(projectPath, 'pom.xml');
  if (!(await pathExists(pomPath))) return null;
  const text = await readTextFile(pomPath);
  const regex = /<dependency>[\s\S]*?<artifactId>(.*?)<\/artifactId>[\s\S]*?<version>(.*?)<\/version>[\s\S]*?<\/dependency>/g;
  const pairs = [];
  let m;
  while ((m = regex.exec(text))) {
    pairs.push([m[1], m[2]]);
  }
  return {
    manager: 'maven',
    label: 'Java (pom.xml)',
    dependencies: toDepMap(pairs),
    devDependencies: {},
    source: pomPath
  };
}

async function parseGradle(projectPath) {
  const gradlePath = path.join(projectPath, 'build.gradle');
  if (!(await pathExists(gradlePath))) return null;
  const lines = (await readTextFile(gradlePath)).split(/\r?\n/);
  const pairs = [];
  const regex = /['"]([^:'"]+:[^:'"]+):([^:'"]+)['"]/;
  for (const line of lines) {
    const m = regex.exec(line);
    if (m) {
      pairs.push([m[1], m[2]]);
    }
  }
  return {
    manager: 'gradle',
    label: 'Java (build.gradle)',
    dependencies: toDepMap(pairs),
    devDependencies: {},
    source: gradlePath
  };
}

async function detectDependencies(projectPath) {
  const parsers = [
    parsePackageJson,
    parseRequirements,
    parseGoMod,
    parseCargoToml,
    parseComposer,
    parsePom,
    parseGradle
  ];
  for (const parser of parsers) {
    const res = await parser(projectPath);
    if (res) return res;
  }
  return null;
}

async function collectProjectInfo(projectPath, options = {}) {
  const { gitUrl } = options;

  const readme = await loadReadme(projectPath);
  const pkg = await loadPackageJson(projectPath);
  const stats = await scanProject(projectPath);
  const depsInfo = await detectDependencies(projectPath);

  const githubInfo = null;

  const profile = detectProfile(pkg ? pkg.json : null, stats, githubInfo);
  const coreNotes = await extractCoreNotes(projectPath, stats.keyFiles);
  const packageManager = await detectPackageManagerFile(projectPath);

  let readmeHtml = null;
  let readmeText = null;
  if (readme && isMeaningfulReadme(readme.content)) {
    readmeText = readme.content;
    readmeHtml = marked.parse(readme.content);
  }

  const projectName = (pkg && pkg.json && pkg.json.name) || path.basename(projectPath);
  const description = (pkg && pkg.json && pkg.json.description) ||
    (readmeText ? firstMeaningfulLine(readmeText) : '项目简介暂未提供，已基于代码结构自动生成。');

  const packageInfo = depsInfo ? {
    manager: depsInfo.manager,
    label: depsInfo.label,
    dependencies: depsInfo.dependencies || {},
    devDependencies: depsInfo.devDependencies || {},
    source: depsInfo.source
  } : null;

  return {
    projectName,
    description,
    readmeHtml,
    readmeText,
    readmePath: readme ? readme.filePath : null,
    packageInfo,
    stats,
    packageManager,
    generatedAt: new Date().toISOString(),
    profile,
    coreNotes,
    githubInfo,
    gitUrl
  };
}

module.exports = {
  collectProjectInfo,
  isMeaningfulReadme,
  scanProject
};
