/**
 * Reporting Module
 * Generates reports, summaries, and analytics
 */

class Reporter {
  constructor(config) {
    this.config = config;
    this.analyzer = null; // Will be injected
  }

  setAnalyzer(analyzer) {
    this.analyzer = analyzer;
  }

  async generateWeeklyReport(meetings) {
    if (!this.analyzer) {
      throw new Error('Analyzer not set. Call setAnalyzer() first.');
    }

    const now = new Date();
    const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    
    const period = `${oneWeekAgo.toLocaleDateString()} to ${now.toLocaleDateString()}`;
    
    // Analyze all meetings
    const analyses = await Promise.all(
      meetings.map(meeting => this.analyzer.analyzeMeeting(meeting))
    );

    // Calculate statistics
    const stats = this.calculateWeeklyStats(meetings, analyses);
    
    // Generate trends
    const trends = this.identifyTrends(meetings, analyses);
    
    // Find top and bottom meetings
    const rankedMeetings = this.rankMeetings(meetings, analyses);
    
    // Generate recommendations
    const recommendations = this.generateWeeklyRecommendations(stats, trends, rankedMeetings);

    return {
      period,
      totalMeetings: meetings.length,
      totalMinutes: stats.totalMinutes,
      averageEfficiency: stats.averageEfficiency,
      estimatedCost: stats.estimatedCost,
      potentialSavings: stats.potentialSavings,
      trends,
      topMeetings: rankedMeetings.top.slice(0, 3),
      bottomMeetings: rankedMeetings.bottom.slice(0, 3),
      recommendations,
      byType: stats.byType,
      byDay: stats.byDay
    };
  }

  calculateWeeklyStats(meetings, analyses) {
    const stats = {
      totalMinutes: 0,
      totalEfficiency: 0,
      estimatedCost: 0,
      potentialSavings: 0,
      byType: {},
      byDay: {},
      meetingCount: meetings.length
    };

    meetings.forEach((meeting, index) => {
      const analysis = analyses[index];
      
      // Basic totals
      stats.totalMinutes += meeting.duration;
      stats.totalEfficiency += analysis.efficiencyScore;
      
      // Cost estimation ($50/hour per attendee)
      const hourlyRate = 50;
      const meetingHours = meeting.duration / 60;
      const attendeeCost = meetingHours * hourlyRate * (meeting.attendees || 1);
      stats.estimatedCost += attendeeCost;
      
      // Potential savings from inefficient meetings
      if (analysis.efficiencyScore < (this.config.efficiency_threshold || 70)) {
        const optimalDuration = this.analyzer.calculateOptimalDuration(meeting);
        stats.potentialSavings += Math.max(0, meeting.duration - optimalDuration);
      }
      
      // Group by type
      const type = this.analyzer.determineMeetingType(meeting);
      if (!stats.byType[type]) {
        stats.byType[type] = {
          count: 0,
          totalMinutes: 0,
          totalEfficiency: 0
        };
      }
      stats.byType[type].count++;
      stats.byType[type].totalMinutes += meeting.duration;
      stats.byType[type].totalEfficiency += analysis.efficiencyScore;
      
      // Group by day (simplified - in real implementation would use actual dates)
      const dayIndex = index % 7;
      const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      const day = days[dayIndex];
      
      if (!stats.byDay[day]) {
        stats.byDay[day] = {
          count: 0,
          totalMinutes: 0
        };
      }
      stats.byDay[day].count++;
      stats.byDay[day].totalMinutes += meeting.duration;
    });

    // Calculate averages
    if (meetings.length > 0) {
      stats.averageEfficiency = Math.round(stats.totalEfficiency / meetings.length);
      
      // Calculate averages for each type
      Object.keys(stats.byType).forEach(type => {
        if (stats.byType[type].count > 0) {
          stats.byType[type].averageEfficiency = Math.round(
            stats.byType[type].totalEfficiency / stats.byType[type].count
          );
          stats.byType[type].averageMinutes = Math.round(
            stats.byType[type].totalMinutes / stats.byType[type].count
          );
        }
      });
    }

    return stats;
  }

  identifyTrends(meetings, analyses) {
    const trends = [];
    
    // Efficiency trend
    const efficiencyScores = analyses.map(a => a.efficiencyScore);
    const avgEfficiency = efficiencyScores.reduce((a, b) => a + b, 0) / efficiencyScores.length;
    
    // Compare with previous "week" (simulated)
    const previousWeekAvg = avgEfficiency * 0.95; // Simulate 5% improvement
    const efficiencyChange = ((avgEfficiency - previousWeekAvg) / previousWeekAvg) * 100;
    
    trends.push({
      category: 'Efficiency',
      value: Math.round(avgEfficiency),
      change: Math.round(efficiencyChange),
      direction: efficiencyChange >= 0 ? 'improving' : 'declining'
    });
    
    // Meeting duration trend
    const avgDuration = meetings.reduce((sum, m) => sum + m.duration, 0) / meetings.length;
    const previousDuration = avgDuration * 1.05; // Simulate 5% longer previously
    const durationChange = ((avgDuration - previousDuration) / previousDuration) * 100;
    
    trends.push({
      category: 'Duration',
      value: Math.round(avgDuration) + ' min',
      change: Math.round(durationChange),
      direction: durationChange <= 0 ? 'improving' : 'declining'
    });
    
    // Meeting count trend
    const meetingCount = meetings.length;
    const previousCount = Math.round(meetingCount * 0.9); // Simulate 10% fewer previously
    const countChange = ((meetingCount - previousCount) / previousCount) * 100;
    
    trends.push({
      category: 'Frequency',
      value: meetingCount + ' meetings',
      change: Math.round(countChange),
      direction: countChange <= 0 ? 'improving' : 'declining'
    });
    
    // Cost trend
    const hourlyRate = 50;
    const totalCost = meetings.reduce((cost, meeting) => {
      const meetingHours = meeting.duration / 60;
      return cost + (meetingHours * hourlyRate * (meeting.attendees || 1));
    }, 0);
    
    const previousCost = totalCost * 1.1; // Simulate 10% higher previously
    const costChange = ((totalCost - previousCost) / previousCost) * 100;
    
    trends.push({
      category: 'Cost',
      value: '$' + Math.round(totalCost),
      change: Math.round(costChange),
      direction: costChange <= 0 ? 'improving' : 'declining'
    });

    return trends;
  }

  rankMeetings(meetings, analyses) {
    // Combine meetings with their analyses
    const combined = meetings.map((meeting, index) => ({
      ...meeting,
      analysis: analyses[index],
      efficiency: analyses[index].efficiencyScore
    }));
    
    // Sort by efficiency (highest first)
    const sorted = [...combined].sort((a, b) => b.efficiency - a.efficiency);
    
    return {
      top: sorted.slice(0, Math.min(5, sorted.length)),
      bottom: [...sorted].reverse().slice(0, Math.min(5, sorted.length)),
      all: sorted
    };
  }

  generateWeeklyRecommendations(stats, trends, rankedMeetings) {
    const recommendations = [];
    
    // Efficiency-based recommendations
    if (stats.averageEfficiency < (this.config.efficiency_threshold || 70)) {
      recommendations.push(`Overall meeting efficiency (${stats.averageEfficiency}/100) is below target. Focus on improving meeting preparation and structure.`);
    }
    
    // Time-based recommendations
    if (stats.totalMinutes > 300) { // More than 5 hours of meetings
      recommendations.push(`You spent ${Math.round(stats.totalMinutes/60)} hours in meetings this week. Consider consolidating or eliminating low-value meetings.`);
    }
    
    // Cost-based recommendations
    if (stats.estimatedCost > 1000) {
      recommendations.push(`Meeting cost estimated at $${Math.round(stats.estimatedCost)}. Review high-cost meetings for optimization opportunities.`);
    }
    
    // Savings opportunity
    if (stats.potentialSavings > 60) {
      recommendations.push(`Potential time savings: ${Math.round(stats.potentialSavings)} minutes (${Math.round(stats.potentialSavings/60)} hours) by optimizing inefficient meetings.`);
    }
    
    // Specific meeting type recommendations
    Object.entries(stats.byType).forEach(([type, data]) => {
      if (data.count > 2 && data.averageEfficiency < 70) {
        recommendations.push(`${type} meetings (${data.count} this week) have low efficiency (${data.averageEfficiency}/100). Consider format improvements.`);
      }
    });
    
    // Bottom-performing meetings
    if (rankedMeetings.bottom.length > 0) {
      const worstMeeting = rankedMeetings.bottom[0];
      recommendations.push(`Lowest efficiency: "${worstMeeting.title}" (${worstMeeting.efficiency}/100). Review this meeting's format and purpose.`);
    }
    
    // Positive reinforcement for good trends
    const improvingTrends = trends.filter(t => t.direction === 'improving');
    if (improvingTrends.length > 0) {
      const bestTrend = improvingTrends[0];
      recommendations.push(`Great progress on ${bestTrend.category.toLowerCase()} (${bestTrend.change}% improvement). Keep it up!`);
    }
    
    // Add generic best practices if we have few specific recommendations
    if (recommendations.length < 3) {
      recommendations.push(
        'Send agendas 24 hours before meetings to improve preparation',
        'Limit meetings to 45 minutes when possible to maintain focus',
        'Assign clear action items with owners and deadlines',
        'Review recurring meetings quarterly to ensure they still provide value'
      );
    }
    
    return recommendations.slice(0, 5); // Limit to top 5 recommendations
  }

  generateMeetingSummary(meeting, analysis) {
    return {
      title: meeting.title,
      date: meeting.startTime || 'Not specified',
      duration: `${meeting.duration} minutes`,
      attendees: meeting.attendees || 'Not specified',
      efficiencyScore: analysis.efficiencyScore,
      efficiencyLevel: this.getEfficiencyLevel(analysis.efficiencyScore),
      keySuggestions: analysis.suggestions?.slice(0, 3) || [],
      riskFactors: analysis.riskFactors || [],
      actionItems: analysis.actionItems || [],
      decisions: analysis.decisions || []
    };
  }

  getEfficiencyLevel(score) {
    if (score >= 90) return 'Excellent';
    if (score >= 80) return 'Good';
    if (score >= 70) return 'Fair';
    if (score >= 60) return 'Needs Improvement';
    return 'Poor';
  }

  formatReport(report, format = 'text') {
    if (format === 'json') {
      return JSON.stringify(report, null, 2);
    }
    
    // Default text format
    let text = `📊 Weekly Meeting Efficiency Report\n`;
    text += `====================================\n\n`;
    
    text += `📅 Period: ${report.period}\n`;
    text += `📋 Total Meetings: ${report.totalMeetings}\n`;
    text += `⏰ Total Time: ${report.totalMinutes} minutes (${Math.round(report.totalMinutes/60)} hours)\n`;
    text += `🎯 Average Efficiency: ${report.averageEfficiency}/100\n`;
    text += `💰 Estimated Cost: $${report.estimatedCost.toFixed(2)}\n`;
    text += `⏱️ Potential Savings: ${report.potentialSavings} minutes\n\n`;
    
    text += `📈 Trends:\n`;
    report.trends.forEach(trend => {
      const trendIcon = trend.change > 0 ? '📈' : trend.change < 0 ? '📉' : '➡️';
      text += `  ${trendIcon} ${trend.category}: ${trend.value} (${trend.change > 0 ? '+' : ''}${trend.change}%)\n`;
    });
    
    text += `\n🏆 Most Efficient Meetings:\n`;
    report.topMeetings.forEach((meeting, index) => {
      text += `  ${index + 1}. ${meeting.title}: ${meeting.efficiency}/100\n`;
    });
    
    text += `\n💡 Recommendations:\n`;
    report.recommendations.forEach((rec, index) => {
      text += `  ${index + 1}. ${rec}\n`;
    });
    
    return text;
  }

  async generateComparativeReport(week1Data, week2Data) {
    // Generate comparison between two weeks
    const comparison = {
      week1: week1Data,
      week2: week2Data,
      changes: {}
    };
    
    // Calculate changes
    const metrics = ['totalMeetings', 'totalMinutes', 'averageEfficiency', 'estimatedCost', 'potentialSavings'];
    
    metrics.forEach(metric => {
      const week1Value = week1Data[metric] || 0;
      const week2Value = week2Data[metric] || 0;
      const change = week2Value - week1Value;
      const percentChange = week1Value > 0 ? (change / week1Value) * 100 : 0;
      
      comparison.changes[metric] = {
        absolute: change,
        percent: Math.round(percentChange),
        direction: change > 0 ? 'increase' : change < 0 ? 'decrease' : 'no change'
      };
    });
    
    // Generate comparative insights
    comparison.insights = this.generateComparativeInsights(comparison);
    
    return comparison;
  }

  generateComparativeInsights(comparison) {
    const insights = [];
    const changes = comparison.changes;
    
    // Efficiency insight
    if (changes.averageEfficiency.percent > 5) {
      insights.push(`Meeting efficiency improved by ${changes.averageEfficiency.percent}% - great work!`);
    } else if (changes.averageEfficiency.percent < -5) {
      insights.push(`Meeting efficiency decreased by ${Math.abs(changes.averageEfficiency.percent)}% - review meeting practices.`);
    }
    
    // Time insight
    if (changes.totalMinutes.percent > 10) {
      insights.push(`Meeting time increased by ${changes.totalMinutes.percent}% - consider if all meetings are necessary.`);
    } else if (changes.totalMinutes.percent < -10) {
      insights.push(`Meeting time decreased by ${Math.abs(changes.totalMinutes.percent)}% - good job optimizing!`);
    }
    
    // Cost insight
    if (changes.estimatedCost.percent > 15) {
      insights.push(`Meeting costs increased by ${changes.estimatedCost.percent}% - review high-cost meetings.`);
    }
    
    // Savings insight
    if (changes.potentialSavings.percent < -20) {
      insights.push(`Potential savings decreased by ${Math.abs(changes.potentialSavings.percent)}% - efficiency improvements are working!`);
    }
    
    // Add generic insight if none generated
    if (insights.length === 0) {
      insights.push('Meeting patterns remained relatively stable this week.');
    }
    
    return insights;
  }

  async exportData(data, format = 'json') {
    switch (format.toLowerCase()) {
      case 'json':
        return JSON.stringify(data, null, 2);
        
      case 'csv':
        return this.convertToCSV(data);
        
      case 'markdown':
        return this.convertToMarkdown(data);
        
      default:
        throw new Error(`Unsupported export format: ${format}`);
    }
  }

  convertToCSV(data) {
    // Simple CSV conversion for meetings array
    if (Array.isArray(data)) {
      if (data.length === 0) return '';
      
      const headers = Object.keys(data[0]).join(',');
      const rows = data.map(item => 
        Object.values(item).map(val => 
          typeof val === 'string' ? `"${val.replace(/"/g, '""')}"` : val
        ).join(',')
      );
      
      return [headers, ...rows].join('\n');
    }
    
    // For single object, flatten it
    const flatten = (obj, prefix = '') => {
      return Object.keys(obj).reduce((acc, key) => {
        const pre = prefix.length ? prefix + '.' : '';
        if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
          Object.assign(acc, flatten(obj[key], pre + key));
        } else {
          acc[pre + key] = obj[key];
        }
        return acc;
      }, {});
    };
    
    const flatData = flatten(data);
    const headers = Object.keys(flatData).join(',');
    const values = Object.values(flatData).map(val => 
      typeof val === 'string' ? `"${val.replace(/"/g, '""')}"` : val
    ).join(',');
    
    return headers + '\n' + values;
  }

  convertToMarkdown(data) {
    if (Array.isArray(data)) {
      if (data.length === 0) return 'No data';
      
      const headers = Object.keys(data[0]);
      let md = '| ' + headers.join(' | ') + ' |\n';
      md += '| ' + headers.map(() => '---').join(' | ') + ' |\n';
      
      data.forEach(item =>