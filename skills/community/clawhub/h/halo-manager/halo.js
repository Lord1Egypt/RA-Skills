#!/usr/bin/env node

/**
 * Halo Manager CLI - 使用官方 @halo-dev/api-client
 * 发布文章到Halo博客
 * 
 * 简化流程：
 * 1. 创建草稿 (POST /api.console.halo.run/v1alpha1/posts)
 * 2. 更新内容 (PUT /api.console.halo.run/v1alpha1/posts/{id}/content)
 * 3. 发布 (PUT /api.console.halo.run/v1alpha1/posts/{id}/publish)
 */

const { createConsoleApiClient } = require('@halo-dev/api-client');
const axios = require('axios');

// 配置
const HALO_URL = process.env.HALO_URL || 'https://yingdong.top';
const HALO_TOKEN = process.env.HALO_TOKEN;

if (!HALO_TOKEN) {
    console.error('请设置 HALO_TOKEN 环境变量');
    console.log('HALO_TOKEN=你的token node halo.js publish "标题" "内容"');
    process.exit(1);
}

// 创建axios实例
const axiosInstance = axios.create({
    baseURL: HALO_URL,
    headers: {
        'Authorization': `Bearer ${HALO_TOKEN}`,
        'Content-Type': 'application/json'
    }
});

// 使用consoleApiClient
const consoleApiClient = createConsoleApiClient(axiosInstance);

// 命令
const command = process.argv[2];
const arg1 = process.argv[3];
const arg2 = process.argv[4];

/**
 * 将Markdown转换为Halo富文本编辑器HTML格式
 */
function markdownToHtml(markdown) {
    let html = markdown;
    
    // 先处理代码块
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code>${code.trim()}</code></pre>`;
    });
    
    // 处理行内代码
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // 处理标题
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
    // 处理粗体和斜体
    html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // 处理链接和图片
    html = html.replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1">');
    html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
    
    // 处理列表 - 转为 <ol><li><p>格式
    const listItems = [];
    html = html.replace(/^[\-\*] (.*$)/gim, (match, text) => {
        listItems.push(text.trim());
        return '___LIST_ITEM___';
    });
    
    // 换行处理 - 用<p>包裹
    const paragraphs = html.split('\n\n');
    let result = '';
    
    for (let p of paragraphs) {
        p = p.trim();
        if (!p) continue;
        
        // 检查是否是列表项
        if (p.includes('___LIST_ITEM___')) {
            let listHtml = '<ol>';
            for (let item of listItems) {
                listHtml += `<li><p style="">${item}</p></li>`;
            }
            listHtml += '</ol>';
            result += listHtml;
        } else {
            // 段落内的换行用<br>
            p = p.replace(/\n/g, '<br>');
            result += `<p style="">${p}</p>`;
        }
    }
    
    return result;
}

async function publishPost(title, content, categories = [], tags = []) {
    const slug = title.toLowerCase()
        .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
        .replace(/^-+|-+$/g, '')
        + '-' + Date.now();

    try {
        console.log('1. 创建文章草稿...');
        
        const htmlContent = markdownToHtml(content);
        
        // 第一步：创建草稿（带HTML内容）
        const postResponse = await consoleApiClient.content.post.draftPost({
            postRequest: {
                post: {
                    spec: {
                        title: title,
                        slug: slug,
                        owner: 'binson',
                        deleted: false,
                        publish: false,
                        pinned: false,
                        allowComment: true,
                        visible: 'PUBLIC',
                        priority: 0,
                        excerpt: { autoGenerate: true, raw: '' },
                        categories: categories,
                        tags: tags
                    },
                    apiVersion: 'content.halo.run/v1alpha1',
                    kind: 'Post',
                    metadata: { 
                        generateName: 'post-',
                        annotations: {
                            'content.halo.run/preferred-editor': 'default'
                        }
                    }
                },
                content: {
                    raw: htmlContent,
                    content: htmlContent,
                    rawType: 'HTML'
                }
            }
        });
        
        const postName = postResponse.data.metadata.name;
        const headSnapshot = postResponse.data.spec.headSnapshot;
        console.log('   草稿创建成功:', postName);
        
        console.log('2. 更新内容...');
        
        // 第二步：更新内容
        await axiosInstance.put(`/apis/api.console.halo.run/v1alpha1/posts/${postName}/content`, {
            raw: htmlContent,
            content: htmlContent,
            rawType: 'HTML',
            snapshotName: headSnapshot
        });
        
        console.log('   内容更新成功');
        
        console.log('3. 发布文章...');
        
        // 第三步：发布
        await consoleApiClient.content.post.publishPost({
            name: postName,
            headSnapshot: headSnapshot
        });
        
        console.log('✅ 文章发布成功!');
        console.log('链接:', `${HALO_URL}/archives/${slug}`);
        
    } catch (error) {
        console.error('发布失败:', error.message);
        if (error.response?.data) {
            console.error('详情:', JSON.stringify(error.response.data, null, 2));
        }
    }
}

async function listPosts() {
    try {
        const response = await consoleApiClient.content.post.listPosts({ size: 20 });
        const data = response.data;
        
        console.log(`共 ${data.total} 篇文章:\n`);
        for (const item of data.items) {
            const title = item.post.spec.title;
            const phase = item.post.status.phase;
            const phaseEmoji = phase === 'PUBLISHED' ? '✅' : '📝';
            console.log(`${phaseEmoji} ${title}`);
        }
    } catch (error) {
        console.error('获取失败:', error.message);
    }
}

async function deletePost(keyword) {
    try {
        const response = await consoleApiClient.content.post.listPosts({ keyword: keyword });
        const data = response.data;
        
        if (data.items.length === 0) {
            console.log('未找到匹配的文章');
            return;
        }
        
        const postName = data.items[0].post.metadata.name;
        
        await consoleApiClient.content.post.deletePostContent({ name: postName });
        console.log('✅ 文章已删除');
        
    } catch (error) {
        console.error('删除失败:', error.message);
    }
}

// 执行命令
switch (command) {
    case 'publish':
        if (!arg1 || !arg2) {
            console.log('用法: halo publish "标题" "内容"');
            console.log('示例: halo publish "我的文章" "这是文章内容"');
            process.exit(1);
        }
        publishPost(arg1, arg2);
        break;
        
    case 'list':
        listPosts();
        break;
        
    case 'delete':
        if (!arg1) {
            console.log('用法: halo delete "关键词"');
            process.exit(1);
        }
        deletePost(arg1);
        break;
        
    default:
        console.log(`
Halo Manager - 文章管理

用法:
  halo publish "标题" "内容"    发布文章
  halo list                      查看文章列表
  halo delete "关键词"          删除文章

环境变量:
  HALO_URL   博客地址 (默认: https://yingdong.top)
  HALO_TOKEN 个人访问令牌 (必须)
`);
}
