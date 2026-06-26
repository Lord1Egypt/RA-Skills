import { useMemo, useState } from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";
import type { CalendarCategory, CalendarDocument } from "../shared/types";

interface StatsViewProps {
    document: CalendarDocument | null;
    categories: CalendarCategory[];
    workingHoursStart: string;
    workingHoursEnd: string;
    workingDays: number[]; // 0=Sun, 1=Mon, etc.
    onClose: () => void;
}

export default function StatsView({
    document,
    categories,
    workingHoursStart,
    workingHoursEnd,
    workingDays,
    onClose
}: StatsViewProps) {
    const [weekOffset, setWeekOffset] = useState(0);

    const stats = useMemo(() => {
        if (!document) return null;

        // Parse working hours
        const [startH, startM] = workingHoursStart.split(":").map(Number);
        const [endH, endM] = workingHoursEnd.split(":").map(Number);

        let capacityMinutes = 0;
        if (!isNaN(startH) && !isNaN(endH) && endH > startH) {
            capacityMinutes = workingDays.length * ((endH * 60 + endM) - (startH * 60 + startM));
        }

        const now = new Date();
        // Monday as start of week
        const currentDay = now.getDay() === 0 ? 7 : now.getDay();
        const startOfWeek = new Date(now);
        startOfWeek.setHours(0, 0, 0, 0);
        startOfWeek.setDate(now.getDate() - (currentDay - 1) + (weekOffset * 7));

        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 7);

        const categoryTotals: Record<string, number> = {};
        let totalScheduledMinutes = 0;

        for (const event of document.events) {
            const eventStart = new Date(event.start);
            const eventEnd = event.end ? new Date(event.end) : new Date(eventStart.getTime() + 60 * 60 * 1000);

            if (eventStart >= endOfWeek || eventEnd <= startOfWeek) {
                continue;
            }

            // Calculate overlap with working hours
            // Simple approximation: if it happens on a working day, and overlaps working hours, add the overlapping minutes.
            let overlapMinutes = 0;

            // We need to iterate day by day for the event because it could span multiple days
            const current = new Date(eventStart);
            while (current < eventEnd && current < endOfWeek) {
                const dayOfWeek = current.getDay(); // 0 is Sunday

                if (workingDays.includes(dayOfWeek)) {
                    // Find overlap for this day
                    const dayStart = new Date(current);
                    dayStart.setHours(startH, startM, 0, 0);

                    const dayEnd = new Date(current);
                    dayEnd.setHours(endH, endM, 0, 0);

                    const overStart = new Date(Math.max(current.getTime(), dayStart.getTime(), startOfWeek.getTime()));

                    let nextCurrent = new Date(current);
                    nextCurrent.setDate(current.getDate() + 1);
                    nextCurrent.setHours(0, 0, 0, 0);

                    const effectiveEventEnd = new Date(Math.min(eventEnd.getTime(), nextCurrent.getTime(), endOfWeek.getTime()));
                    const overEnd = new Date(Math.min(effectiveEventEnd.getTime(), dayEnd.getTime()));

                    if (overEnd > overStart) {
                        overlapMinutes += (overEnd.getTime() - overStart.getTime()) / (1000 * 60);
                    }
                }

                // Move to next day
                current.setDate(current.getDate() + 1);
                current.setHours(0, 0, 0, 0);
            }

            if (overlapMinutes > 0) {
                if (!categoryTotals[event.category]) {
                    categoryTotals[event.category] = 0;
                }
                categoryTotals[event.category] += overlapMinutes;
                totalScheduledMinutes += overlapMinutes;
            }
        }

        const freeMinutes = Math.max(0, capacityMinutes - totalScheduledMinutes);

        const data = [];
        for (const cat of categories) {
            const mins = categoryTotals[cat.id] || 0;
            data.push({
                name: cat.label,
                value: Math.round(mins / 60 * 10) / 10, // hours
                color: cat.color || "#8884d8",
                minutes: mins
            });
        }

        // Add any events that have category IDs not in the predefined categories list
        for (const [catId, mins] of Object.entries(categoryTotals)) {
            if (!categories.find(c => c.id === catId)) {
                data.push({
                    name: catId,
                    value: Math.round(mins / 60 * 10) / 10,
                    color: "#8884d8",
                    minutes: mins
                });
            }
        }

        if (freeMinutes > 0) {
            data.push({
                name: "Free Time",
                value: Math.round(freeMinutes / 60 * 10) / 10,
                color: "#e2e8f0",
                minutes: freeMinutes
            });
        }

        data.sort((a, b) => b.value - a.value);

        return {
            data,
            capacityMinutes,
            totalScheduledMinutes,
            freeMinutes,
            startDate: startOfWeek,
            endDate: new Date(endOfWeek.getTime() - 1)
        };
    }, [document, workingHoursStart, workingHoursEnd, workingDays, weekOffset, categories]);

    if (!document || !stats) {
        return <div className="settings-page">Loading...</div>;
    }

    const { data, startDate, endDate, capacityMinutes, totalScheduledMinutes, freeMinutes } = stats;

    return (
        <div className="settings-page">
            <header className="settings-header">
                <h2>Weekly Stats</h2>
                <button className="ghost-btn" onClick={onClose}>
                    Done
                </button>
            </header>

            <div className="settings-grid">
                <div className="settings-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button className="ghost-btn" onClick={() => setWeekOffset(o => o - 1)}>← Previous Week</button>
                    <div style={{ fontWeight: 500 }}>
                        {startDate.toLocaleDateString()} - {endDate.toLocaleDateString()}
                    </div>
                    <button className="ghost-btn" onClick={() => setWeekOffset(o => o + 1)}>Next Week →</button>
                </div>

                <div className="settings-card" style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
                    <div style={{ flex: '1 1 300px', minHeight: '300px' }}>
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={data}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={100}
                                    paddingAngle={2}
                                    dataKey="value"
                                >
                                    {data.map((entry: any, index: number) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    formatter={(value: any) => [`${value} hrs`, "Time"]}
                                    contentStyle={{ borderRadius: '8px', border: '1px solid var(--line)' }}
                                />
                                <Legend layout="horizontal" verticalAlign="bottom" align="center" />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>

                    <div style={{ flex: '1 1 200px', display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '1rem' }}>
                        <div>
                            <div style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>Working Capacity</div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{Math.round(capacityMinutes / 60 * 10) / 10} hrs</div>
                        </div>
                        <div>
                            <div style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>Scheduled Time</div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{Math.round(totalScheduledMinutes / 60 * 10) / 10} hrs</div>
                        </div>
                        <div>
                            <div style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>Free Time</div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 600, color: '#10b981' }}>{Math.round(freeMinutes / 60 * 10) / 10} hrs</div>
                        </div>
                    </div>
                </div>

                <div className="settings-card">
                    <h3>Breakdown</h3>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid var(--line)', textAlign: 'left', color: 'var(--muted)' }}>
                                <th style={{ padding: '0.5rem 0', fontWeight: 500 }}>Category</th>
                                <th style={{ padding: '0.5rem 0', fontWeight: 500, textAlign: 'right' }}>Hours</th>
                                <th style={{ padding: '0.5rem 0', fontWeight: 500, textAlign: 'right' }}>% of Capacity</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((item: any, i: number) => (
                                <tr key={i} style={{ borderBottom: '1px solid var(--line)' }}>
                                    <td style={{ padding: '0.75rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <span style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: item.color, display: 'inline-block' }}></span>
                                        {item.name}
                                    </td>
                                    <td style={{ padding: '0.75rem 0', textAlign: 'right', fontWeight: 500 }}>{item.value}</td>
                                    <td style={{ padding: '0.75rem 0', textAlign: 'right', color: 'var(--muted)' }}>
                                        {capacityMinutes > 0 ? Math.round((item.minutes / capacityMinutes) * 100) : 0}%
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
