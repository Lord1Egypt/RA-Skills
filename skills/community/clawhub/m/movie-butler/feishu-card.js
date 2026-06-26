#!/usr/bin/env node

/**
 * 🎬 飞书卡片推送 - 观影小管家专用
 * 发送电影推荐卡片到飞书
 */

const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../../../.env') });

const EMBY_URL = process.env.EMBY_URL || 'http://192.168.0.151:8096';

function buildMovieCard(movie, embyItem, recommendation = null) {
    const year = movie.release_date?.split('-')[0] || '未知';
    const rating = movie.vote_average?.toFixed(1) || 'N/A';
    const genres = movie.genres?.map(g => g.name).join('、') || '未知';
    const overview = movie.overview ? (movie.overview.substring(0, 200) + '...') : '暂无简介';
    
    const card = {
        config: { wide_screen_mode: true },
        header: {
            title: { tag: 'plain_text', content: `🎬 ${movie.title} (${year})` },
            template: recommendation ? 'green' : 'blue'
        },
        elements: []
    };
    
    // 评分信息
    const ratingBlock = {
        tag: 'div',
        fields: [
            {
                is_short: true,
                text: { tag: 'lark_md', content: `⭐ **评分**\n${rating}/10` }
            },
            {
                is_short: true,
                text: { tag: 'lark_md', content: `🎭 **类型**\n${genres}` }
            }
        ]
    };
    card.elements.push(ratingBlock);
    
    // 服务器状态
    if (embyItem) {
        const embyId = embyItem.Id;
        const playUrl = `${EMBY_URL}/web/index.html#!/item?id=${embyId}&serverId=${embyItem.ServerId}`;
        
        const statusBlock = {
            tag: 'div',
            text: {
                tag: 'lark_md',
                content: `📺 **服务器状态**: ✅ 已有\n🔗 [▶️ 点击播放](${playUrl})`
            }
        };
        card.elements.push(statusBlock);
    } else {
        const statusBlock = {
            tag: 'div',
            text: {
                tag: 'lark_md',
                content: `📺 **服务器状态**: ❌ 暂无\n💡 建议手动下载添加到服务器`
            }
        };
        card.elements.push(statusBlock);
    }
    
    // 简介
    const overviewBlock = {
        tag: 'div',
        text: {
            tag: 'lark_md',
            content: `📝 **简介**\n${overview}`
        }
    };
    card.elements.push(overviewBlock);
    
    // 推荐理由（如果有）
    if (recommendation) {
        const reasonBlock = {
            tag: 'div',
            text: {
                tag: 'lark_md',
                content: `💡 **推荐理由**\n${recommendation}`
            }
        };
        card.elements.push(reasonBlock);
    }
    
    // 海报（如果有）
    if (movie.poster_path) {
        const imageBlock = {
            tag: 'img',
            img_key: '', // 需要上传
            alt: { tag: 'plain_text', content: `${movie.title} 海报` },
            mode: 'fit_vertical',
            preview: true
        };
        card.elements.push(imageBlock);
    }
    
    return card;
}

module.exports = { buildMovieCard };
