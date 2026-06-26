/**
 * Tasks - List pending tasks
 * Usage: node scripts/tasks.js [status]
 * Default status: pending
 */

const { makeRequest } = require('./api');

async function listTasks() {
    const status = process.argv[2] || '';
    const endpoint = status ? `/tasks?status=${status}` : '/tasks';

    try {
        const r = await makeRequest('GET', endpoint);
        const tasks = Array.isArray(r.data) ? r.data : (r.data?.tasks || []);
        const pending = tasks.filter(t => !t.completed && !t.isCompleted);

        if (pending.length === 0) {
            console.log('✅ No pending tasks!');
            return;
        }

        console.log(`📋 *Tasks Pending* (${pending.length})\n`);

        const priorityIcon = { high: '🔴', medium: '🟡', low: '🟢' };

        pending.forEach(t => {
            const icon = priorityIcon[t.priority] || '⚪';
            const dueDate = t.dueDate || t.due_date || t.deadline;
            let dueStr = '';
            if (dueDate) {
                const days = Math.ceil((new Date(dueDate) - new Date()) / (1000 * 60 * 60 * 24));
                dueStr = days < 0 ? ` ⏰ ${Math.abs(days)} day(s) overdue!` : days === 0 ? ' ⏰ Due today!' : days === 1 ? ' ⏰ Tomorrow' : ` 📅 ${days} days left`;
            }
            console.log(`${icon} ${t.title || t.name}${dueStr}`);
            if (t.Project?.name || t.project_name) console.log(`   📁 ${t.Project?.name || t.project_name}`);
        });
    } catch (err) {
        console.error('❌', err.message);
    }
}

listTasks();
