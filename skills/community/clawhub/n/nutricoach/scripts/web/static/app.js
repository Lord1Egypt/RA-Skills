// NutriCoach Dashboard JavaScript

let currentItemId = null;
let currentItemName = null;
let currentItemRemaining = 0;
let currentItemUnit = 'g';
let currentShelfLife = 7;
let pantryViewMode = 'location';
let pantryData = null;

// Tab switching
function showTab(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(tabName).classList.add('active');
    if (tabName === 'pantry') loadPantry();
}

// Load overview data
fetch('/api/summary').then(r => r.json()).then(data => {
    const daily = data.daily?.data || {};
    document.getElementById('daily-summary').innerHTML = `
        <div class="stat"><span>热量</span><span class="stat-value">${Math.round(daily.totals?.calories || 0)}/${Math.round(daily.tdee || 2000)} kcal</span></div>
        <div class="stat"><span>蛋白质</span><span class="stat-value">${Math.round(daily.totals?.protein_g || 0)}g</span></div>
        <div class="stat"><span>碳水</span><span class="stat-value">${Math.round(daily.totals?.carbs_g || 0)}g</span></div>
        <div class="stat"><span>脂肪</span><span class="stat-value">${Math.round(daily.totals?.fat_g || 0)}g</span></div>
    `;
});

// Load profile
fetch('/api/profile').then(r => r.json()).then(data => {
    const p = data.data || {};
    document.getElementById('profile').innerHTML = `
        <div class="stat"><span>身高</span><span class="stat-value">${p.height_cm} cm</span></div>
        <div class="stat"><span>BMR</span><span class="stat-value">${Math.round(p.bmr || 0)} kcal</span></div>
        <div class="stat"><span>TDEE</span><span class="stat-value">${Math.round(p.tdee || 0)} kcal</span></div>
        <div class="stat"><span>目标</span><span class="stat-value">${p.goal_type === 'lose' ? '减脂' : p.goal_type === 'gain' ? '增肌' : '维持'}</span></div>
    `;
});

// Load weight history and render chart
fetch('/api/weight-history?days=30').then(r => r.json()).then(data => {
    if (data.status === 'success' && data.data?.records?.length > 0) {
        // Take last 30 records, reverse to show chronological order (earliest first)
        const records = data.data.records.slice(-30).reverse();
        const labels = records.map(r => r.recorded_at?.slice(5, 10) || '');
        const weights = records.map(r => r.weight_kg);

        new Chart(document.getElementById('weightChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: '体重 (kg)',
                    data: weights,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    } else {
        document.getElementById('weightChart').parentElement.innerHTML = '<p style="text-align:center;color:#999;padding:40px;">暂无体重数据</p>';
    }
});

// Load nutrition history and render chart
fetch('/api/nutrition-history?days=7').then(r => r.json()).then(data => {
    if (data.status === 'success' && data.data?.meals?.length > 0) {
        const meals = data.data.meals;
        
        // Group meals by date and sum nutrients
        const dailyTotals = {};
        meals.forEach(meal => {
            const date = meal.eaten_at?.slice(0, 10) || '';
            if (!date) return;
            
            if (!dailyTotals[date]) {
                dailyTotals[date] = { calories: 0, protein: 0, carbs: 0, fat: 0 };
            }
            dailyTotals[date].calories += meal.total_calories || 0;
            dailyTotals[date].protein += meal.total_protein_g || 0;
            dailyTotals[date].carbs += meal.total_carbs_g || 0;
            dailyTotals[date].fat += meal.total_fat_g || 0;
        });
        
        // Convert to array and sort by date
        const days = Object.entries(dailyTotals)
            .map(([date, totals]) => ({ date, ...totals }))
            .sort((a, b) => new Date(a.date) - new Date(b.date));
        
        if (days.length === 0) {
            document.getElementById('nutritionChart').parentElement.innerHTML = '<p style="text-align:center;color:#999;padding:40px;">暂无营养数据</p>';
            return;
        }
        
        const labels = days.map(d => d.date?.slice(5, 10) || '');
        const calories = days.map(d => d.calories || 0);
        const protein = days.map(d => d.protein || 0);
        const carbs = days.map(d => d.carbs || 0);
        const fat = days.map(d => d.fat || 0);

        new Chart(document.getElementById('nutritionChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: '热量 (kcal)',
                        data: calories,
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.3,
                        fill: true,
                        yAxisID: 'y'
                    },
                    {
                        label: '蛋白质 (g)',
                        data: protein,
                        borderColor: '#4caf50',
                        backgroundColor: 'rgba(76, 175, 80, 0.1)',
                        tension: 0.3,
                        fill: false,
                        yAxisID: 'y1'
                    },
                    {
                        label: '碳水 (g)',
                        data: carbs,
                        borderColor: '#ff9800',
                        backgroundColor: 'rgba(255, 152, 0, 0.1)',
                        tension: 0.3,
                        fill: false,
                        yAxisID: 'y1'
                    },
                    {
                        label: '脂肪 (g)',
                        data: fat,
                        borderColor: '#f44336',
                        backgroundColor: 'rgba(244, 67, 54, 0.1)',
                        tension: 0.3,
                        fill: false,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { 
                    legend: { 
                        display: true,
                        position: 'top',
                        labels: { font: { size: 11 } }
                    } 
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: { display: true, text: '热量 (kcal)' },
                        grid: { color: 'rgba(0,0,0,0.05)' }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: { display: true, text: '营养素 (g)' },
                        grid: { drawOnChartArea: false }
                    }
                }
            }
        });
    } else {
        document.getElementById('nutritionChart').parentElement.innerHTML = '<p style="text-align:center;color:#999;padding:40px;">暂无营养数据</p>';
    }
});

// Pantry view switching
function showPantryView(mode) {
    pantryViewMode = mode;
    document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    renderPantry();
}

// Get expiry badge
function getExpiryBadge(item) {
    if (!item.expiry_date) return { class: 'expiry-ok', text: '新鲜' };
    const today = new Date();
    today.setHours(0, 0, 0, 0);  // 只比较日期部分
    const expiry = new Date(item.expiry_date);
    expiry.setHours(0, 0, 0, 0);
    const daysLeft = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24));
    
    if (daysLeft < 0) return { class: 'expiry-expired', text: '已过期' };
    if (daysLeft === 0) return { class: 'expiry-urgent', text: '今天' };
    if (daysLeft === 1) return { class: 'expiry-urgent', text: '明天' };
    if (daysLeft <= 3) return { class: 'expiry-soon', text: `${daysLeft}天` };
    return { class: 'expiry-ok', text: `${daysLeft}天` };
}

// Location name mapping
const LOCATION_NAMES = {
    'fridge': '冰箱',
    'freezer': '冷冻',
    'pantry': '干货区',
    'counter': '台面'
};

// Category mapping
const CATEGORY_MAP = {
    'protein': '蛋白质',
    'vegetable': '蔬菜',
    'carb': '碳水',
    'fruit': '水果',
    'dairy': '乳制品',
    'fat': '脂肪',
    'other': '其他'
};

// Render pantry item
function renderItem(item) {
    const expiry = getExpiryBadge(item);
    const percent = Math.round((item.remaining_g / item.initial_g) * 100);
    const progressClass = percent > 50 ? 'pantry-progress-high' : percent > 20 ? 'pantry-progress-medium' : 'pantry-progress-low';
    const unit = item.unit || 'g';
    const locationName = LOCATION_NAMES[item.location] || item.location || '冰箱';
    const category = item.category || 'other';
    // Escape food name for use in onclick attribute
    const escapedFoodName = item.food_name.replace(/'/g, "\\'").replace(/"/g, '\\"');

    return `
        <div class="pantry-item">
            <div class="pantry-item-header">
                <div class="pantry-info">
                    <div class="pantry-name" title="${item.food_name}">${item.food_name}</div>
                    <div class="pantry-qty">${item.remaining_g}${unit}</div>
                </div>
                <div class="pantry-actions">
                    <span class="expiry-badge ${expiry.class}">${expiry.text}</span>
                    <button class="action-btn" onclick="openEditModal(${item.id}, '${escapedFoodName}', ${item.remaining_g}, '${unit}', ${item.shelf_life_days || 7}, '${item.purchase_date || ''}', '${item.expiry_date || ''}', '${locationName}', '${category}')">编辑</button>
                </div>
            </div>
            <div class="pantry-progress">
                <div class="pantry-progress-bar ${progressClass}" style="width: ${percent}%"></div>
            </div>
        </div>
    `;
}

// Render pantry
function renderPantry() {
    if (!pantryData) return;
    let html = '';

    if (pantryViewMode === 'location') {
        const locationNames = {'冰箱': '冰箱', '冷冻': '冷冻', '干货区': '干货区', '台面': '台面'};
        for (const [location, items] of Object.entries(pantryData.grouped || {})) {
            if (items.length === 0) continue;
            html += `<div class="location-section">`;
            html += `<div class="location-title">${locationNames[location]} (${items.length})</div>`;
            html += `<div class="pantry-grid">`;
            for (const item of items) html += renderItem(item);
            html += `</div></div>`;
        }
    } else {
        const categoryIcons = {'蛋白质': '', '蔬菜': '', '碳水': '', '水果': '', '乳制品': '', '脂肪': '', '其他': ''};
        for (const [category, items] of Object.entries(pantryData.by_category || {})) {
            if (items.length === 0) continue;
            html += `<div class="location-section">`;
            html += `<div class="location-title">${categoryIcons[category]} ${category} (${items.length})</div>`;
            html += `<div class="pantry-grid">`;
            for (const item of items) html += renderItem(item);
            html += `</div></div>`;
        }
    }
    document.getElementById('pantry-content').innerHTML = html;
}

// Load pantry
function loadPantry() {
    fetch('/api/pantry').then(r => r.json()).then(data => {
        if (data.status !== 'success') {
            document.getElementById('pantry-content').innerHTML = '<p>加载失败</p>';
            return;
        }
        pantryData = data.data;
        renderPantry();
    });
}

// Calculate expiry
function calculateExpiry() {
    const purchase = document.getElementById('editPurchase').value;
    const shelfLife = parseInt(document.getElementById('editShelfLife').value);
    const expirySpan = document.getElementById('editCalculatedExpiry');
    if (purchase && shelfLife > 0) {
        const pDate = new Date(purchase);
        const eDate = new Date(pDate.getTime() + shelfLife * 24 * 60 * 60 * 1000);
        expirySpan.textContent = eDate.toLocaleDateString('zh-CN');
    } else {
        expirySpan.textContent = '-';
    }
}

// Modal functions
function openEditModal(id, name, remaining, unit, shelfLife, purchase, expiry, location, category) {
    currentItemId = id;
    currentItemName = name;
    currentItemRemaining = remaining;
    currentItemUnit = unit || 'g';
    currentShelfLife = shelfLife;
    document.getElementById('editModalItemName').textContent = `${name} (剩余 ${remaining}${currentItemUnit})`;
    document.getElementById('editUseAmount').placeholder = `使用重量 (${currentItemUnit})`;
    document.getElementById('editUseAmount').value = '';
    document.getElementById('editPurchase').value = purchase || '';
    document.getElementById('editShelfLife').value = shelfLife || 7;
    document.getElementById('editLocation').value = location || '冰箱';
    document.getElementById('editCategory').value = category || 'other';
    calculateExpiry();
    document.getElementById('editModal').classList.add('active');
}

function openAddModal() {
    document.getElementById('addFoodName').value = '';
    document.getElementById('addQuantity').value = '';
    document.getElementById('addExpiry').value = '';
    document.getElementById('addLocation').value = 'auto';
    document.getElementById('addModal').classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

function confirmUseFromEdit() {
    const amount = parseFloat(document.getElementById('editUseAmount').value);
    const unit = currentItemUnit || 'g';
    if (!amount || amount <= 0) {
        alert('请输入有效的使用量');
        return;
    }
    if (amount > currentItemRemaining) {
        alert(`使用量不能超过剩余量 (${currentItemRemaining}${unit})`);
        return;
    }
    fetch('/api/pantry/use', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: currentItemId, amount: amount })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            showSuccess(`已记录：使用 ${amount}${unit} ${currentItemName}`);
            currentItemRemaining -= amount;
            document.getElementById('editModalItemName').textContent = `${currentItemName} (剩余 ${currentItemRemaining}${unit})`;
            document.getElementById('editUseAmount').value = '';
            setTimeout(loadPantry, 500);
        } else {
            alert('失败：' + (data.message || data.error));
        }
    });
}

function confirmEdit() {
    const purchase = document.getElementById('editPurchase').value;
    const shelfLife = parseInt(document.getElementById('editShelfLife').value);
    const location = document.getElementById('editLocation').value;

    const body = { item_id: currentItemId };
    if (purchase) body.purchase = purchase;
    if (shelfLife > 0) body.shelf_life = shelfLife;
    if (location) body.location = location;

    fetch('/api/pantry/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            showSuccess(`已更新：${currentItemName}`);
            closeModal('editModal');
            setTimeout(loadPantry, 500);
        } else {
            alert('失败：' + (data.message || data.error));
        }
    });
}

function confirmDelete() {
    if (!currentItemId) {
        alert('未选择食材');
        return;
    }
    
    if (!confirm(`确定要删除 "${currentItemName}" 吗？此操作不可恢复。`)) {
        return;
    }
    
    fetch('/api/pantry/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: currentItemId })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            showSuccess(`已删除：${currentItemName}`);
            closeModal('editModal');
            setTimeout(loadPantry, 500);
        } else {
            alert('删除失败：' + (data.message || data.error));
        }
    });
}

function confirmAdd() {
    const food = document.getElementById('addFoodName').value.trim();
    const quantity = parseFloat(document.getElementById('addQuantity').value);
    const expiry = document.getElementById('addExpiry').value;
    const location = document.getElementById('addLocation').value;

    if (!food || !quantity) {
        alert('请填写完整信息');
        return;
    }

    const body = { food: food, quantity: quantity, location: location };
    if (expiry) body.expiry = expiry;

    fetch('/api/pantry/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            showSuccess(`已添加：${food}`);
            closeModal('addModal');
            setTimeout(loadPantry, 500);
        } else {
            alert('失败：' + (data.message || data.error));
        }
    });
}

function showSuccess(msg) {
    const el = document.getElementById('success-msg');
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(() => el.style.display = 'none', 3000);
}

// Auto-calculate expiry when inputs change
document.addEventListener('DOMContentLoaded', function() {
    const purchaseInput = document.getElementById('editPurchase');
    const shelfLifeInput = document.getElementById('editShelfLife');
    if (purchaseInput) purchaseInput.addEventListener('change', calculateExpiry);
    if (shelfLifeInput) shelfLifeInput.addEventListener('input', calculateExpiry);
});

window.onclick = function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
};
