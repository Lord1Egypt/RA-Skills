/**
 * AI Analysis Module
 * Handles meeting analysis, efficiency scoring, and note processing
 */

class Analyzer {
  constructor(config) {
    this.config = config;
    this.aiProvider = config.ai_provider || 'openai';
    this.aiApiKey = config.ai_api_key || '';
    this.efficiencyThreshold = config.efficiency_threshold || 70;
  }

  async analyzeMeeting(meeting) {
    // Analyze a meeting and provide efficiency score and suggestions
    
    const analysis = {
      meetingId: meeting.id,
      title: meeting.title,
      efficiencyScore: this.calculateEfficiencyScore(meeting),
      meetingType: this.determineMeetingType(meeting),
      optimalDuration: this.calculateOptimalDuration(meeting),
      suggestions: this.generateSuggestions(meeting),
      recommendations: [],
      riskFactors: []
    };

    // Add AI-powered analysis if API key is available
    if (this.aiApiKey) {
      try {
        const aiAnalysis = await this.getAIAnalysis(meeting);
        Object.assign(analysis, aiAnalysis);
      } catch (error) {
        console.warn('AI analysis failed, using rule-based analysis:', error.message);
      }
    }

    // Add risk factors
    analysis.riskFactors = this.identifyRiskFactors(meeting);

    return analysis;
  }

  calculateEfficiencyScore(meeting) {
    // Calculate efficiency score based on multiple factors
    let score = 80; // Base score

    // Adjust based on duration
    const optimalDuration = this.calculateOptimalDuration(meeting);
    const durationRatio = optimalDuration / meeting.duration;
    
    if (durationRatio < 0.8) {
      score -= 20; // Meeting too long
    } else if (durationRatio > 1.2) {
      score -= 10; // Meeting too short
    }

    // Adjust based on attendees
    const optimalAttendees = this.calculateOptimalAttendees(meeting);
    if (meeting.attendees > optimalAttendees * 1.5) {
      score -= 15; // Too many attendees
    } else if (meeting.attendees < optimalAttendees * 0.5) {
      score -= 5; // Too few attendees
    }

    // Adjust based on meeting type
    const type = this.determineMeetingType(meeting);
    if (type === 'decision') {
      // Decision meetings should have clear outcomes
      if (!meeting.description || !meeting.description.toLowerCase().includes('decision')) {
        score -= 10;
      }
    } else if (type === 'brainstorming') {
      // Brainstorming should have participation goals
      if (!meeting.description || !meeting.description.toLowerCase().includes('ideas')) {
        score -= 5;
      }
    }

    // Ensure score is between 0-100
    return Math.max(0, Math.min(100, Math.round(score)));
  }

  determineMeetingType(meeting) {
    const title = (meeting.title || '').toLowerCase();
    const description = (meeting.description || '').toLowerCase();

    if (title.includes('standup') || title.includes('daily') || title.includes('scrum')) {
      return 'standup';
    } else if (title.includes('review') || description.includes('review')) {
      return 'review';
    } else if (title.includes('planning') || description.includes('planning')) {
      return 'planning';
    } else if (title.includes('brainstorm') || description.includes('brainstorm')) {
      return 'brainstorming';
    } else if (title.includes('decision') || description.includes('decision')) {
      return 'decision';
    } else if (title.includes('client') || description.includes('client')) {
      return 'client';
    } else if (title.includes('training') || description.includes('training')) {
      return 'training';
    } else {
      return 'general';
    }
  }

  calculateOptimalDuration(meeting) {
    const type = this.determineMeetingType(meeting);
    const attendees = meeting.attendees || 1;

    // Base optimal durations by meeting type
    const baseDurations = {
      standup: 15,
      review: 30,
      planning: 60,
      brainstorming: 45,
      decision: 30,
      client: 60,
      training: 90,
      general: 30
    };

    let optimal = baseDurations[type] || 30;

    // Adjust for number of attendees
    if (attendees > 10) {
      optimal *= 1.5;
    } else if (attendees > 5) {
      optimal *= 1.2;
    }

    return Math.round(optimal);
  }

  calculateOptimalAttendees(meeting) {
    const type = this.determineMeetingType(meeting);
    
    const optimalByType = {
      standup: 8,
      review: 5,
      planning: 4,
      brainstorming: 6,
      decision: 3,
      client: 3,
      training: 15,
      general: 5
    };

    return optimalByType[type] || 5;
  }

  generateSuggestions(meeting) {
    const suggestions = [];
    const efficiencyScore = this.calculateEfficiencyScore(meeting);
    const optimalDuration = this.calculateOptimalDuration(meeting);
    const optimalAttendees = this.calculateOptimalAttendees(meeting);

    // Duration suggestions
    if (meeting.duration > optimalDuration * 1.2) {
      suggestions.push(`Consider reducing duration from ${meeting.duration} to ${optimalDuration} minutes`);
    } else if (meeting.duration < optimalDuration * 0.8) {
      suggestions.push(`Consider increasing duration from ${meeting.duration} to ${optimalDuration} minutes for better outcomes`);
    }

    // Attendee suggestions
    if (meeting.attendees > optimalAttendees * 1.5) {
      suggestions.push(`Reduce attendees from ${meeting.attendees} to ${optimalAttendees} for more effective discussion`);
    } else if (meeting.attendees < optimalAttendees * 0.5) {
      suggestions.push(`Consider inviting more participants (current: ${meeting.attendees}, optimal: ${optimalAttendees})`);
    }

    // Agenda suggestions
    if (!meeting.description || meeting.description.length < 20) {
      suggestions.push('Add a clear agenda to the meeting description');
    }

    // Recurring meeting optimization
    if (meeting.recurring && efficiencyScore < this.efficiencyThreshold) {
      suggestions.push('Review recurring meeting format - consider adjustments to improve efficiency');
    }

    // Time of day suggestions
    const hour = parseInt(meeting.startTime?.split(':')[0] || '12');
    if (hour < 9 || hour > 16) {
      suggestions.push('Consider scheduling during core working hours (9 AM - 5 PM)');
    }

    return suggestions;
  }

  identifyRiskFactors(meeting) {
    const risks = [];
    const efficiencyScore = this.calculateEfficiencyScore(meeting);

    if (efficiencyScore < 50) {
      risks.push('High risk of inefficiency');
    } else if (efficiencyScore < this.efficiencyThreshold) {
      risks.push('Moderate risk of inefficiency');
    }

    if (meeting.duration > 120) {
      risks.push('Long duration may lead to fatigue');
    }

    if (meeting.attendees > 15) {
      risks.push('Large group may reduce individual participation');
    }

    if (!meeting.description || meeting.description.length < 10) {
      risks.push('Lack of agenda increases risk of unfocused meeting');
    }

    return risks;
  }

  async processMeetingNotes(notes) {
    // Process meeting notes to extract key information
    
    const result = {
      summary: [],
      actionItems: [],
      decisions: [],
      questions: [],
      efficiencyScore: 0,
      participants: []
    };

    // Simple text analysis for demo
    // In production, this would use AI for better extraction
    
    const lines = notes.split('\n').filter(line => line.trim());
    
    lines.forEach(line => {
      const trimmed = line.trim().toLowerCase();
      
      // Extract action items (lines with TODO, ACTION, or task indicators)
      if (trimmed.includes('todo') || trimmed.includes('action') || 
          trimmed.includes('task') || trimmed.includes('follow up')) {
        result.actionItems.push({
          text: line.trim(),
          owner: this.extractOwner(line),
          dueDate: this.extractDueDate(line),
          priority: this.extractPriority(line)
        });
      }
      
      // Extract decisions (lines with decided, agree, will)
      else if (trimmed.includes('decided') || trimmed.includes('agree') || 
               trimmed.includes('will') || trimmed.includes('agreed')) {
        result.decisions.push(line.trim());
      }
      
      // Extract questions (lines with ?, question, or unsure)
      else if (trimmed.includes('?') || trimmed.includes('question') || 
               trimmed.includes('unsure') || trimmed.includes('tbd')) {
        result.questions.push(line.trim());
      }
      
      // Otherwise, add to summary (key points)
      else if (line.length > 10 && !trimmed.startsWith('-') && !trimmed.startsWith('•')) {
        result.summary.push(line.trim());
      }
    });

    // Limit summary to 5 key points
    if (result.summary.length > 5) {
      result.summary = result.summary.slice(0, 5);
    }

    // Calculate efficiency based on notes quality
    result.efficiencyScore = this.calculateNotesEfficiency(notes, result);

    // Extract participants if mentioned
    result.participants = this.extractParticipants(notes);

    return result;
  }

  extractOwner(line) {
    // Simple owner extraction
    const match = line.match(/@(\w+)|(\w+):/);
    return match ? (match[1] || match[2] || 'Unassigned') : 'Unassigned';
  }

  extractDueDate(line) {
    // Simple date extraction
    const dateMatch = line.match(/(\d{1,2}\/\d{1,2}\/\d{2,4})|(\d{4}-\d{2}-\d{2})|(next week|tomorrow|today)/i);
    return dateMatch ? dateMatch[0] : 'No deadline';
  }

  extractPriority(line) {
    if (line.toLowerCase().includes('high') || line.includes('!!!')) return 'High';
    if (line.toLowerCase().includes('medium') || line.includes('!!')) return 'Medium';
    if (line.toLowerCase().includes('low') || line.includes('!')) return 'Low';
    return 'Medium';
  }

  calculateNotesEfficiency(notes, extracted) {
    let score = 70; // Base score
    
    // Points for having action items
    if (extracted.actionItems.length > 0) {
      score += 10;
    }
    
    // Points for having decisions
    if (extracted.decisions.length > 0) {
      score += 10;
    }
    
    // Penalty for unresolved questions
    if (extracted.questions.length > 3) {
      score -= 10;
    }
    
    // Points for clear summary
    if (extracted.summary.length >= 3) {
      score += 10;
    }
    
    // Penalty for very short notes
    if (notes.length < 50) {
      score -= 20;
    }
    
    return Math.max(0, Math.min(100, score));
  }

  extractParticipants(notes) {
    // Simple participant extraction
    const participants = [];
    const lines = notes.split('\n');
    
    lines.forEach(line => {
      // Look for lines that might list participants
      if (line.toLowerCase().includes('attendees') || 
          line.toLowerCase().includes('participants') ||
          line.toLowerCase().includes('present:')) {
        const parts = line.split(':');
        if (parts.length > 1) {
          const names = parts[1].split(/[,&]/);
          names.forEach(name => {
            const trimmed = name.trim();
            if (trimmed && trimmed.length > 1) {
              participants.push(trimmed);
            }
          });
        }
      }
    });
    
    return participants.length > 0 ? participants : ['Participants not listed'];
  }

  async getAIAnalysis(meeting) {
    // This would call OpenAI/Grok API for advanced analysis
    // For now, return enhanced rule-based analysis
    
    return {
      aiEnhanced: true,
      sentiment: this.analyzeSentiment(meeting),
      complexity: this.assessComplexity(meeting),
      preparationScore: this.calculatePreparationScore(meeting),
      aiSuggestions: this.generateAISuggestions(meeting)
    };
  }

  analyzeSentiment(meeting) {
    const title = (meeting.title || '').toLowerCase();
    const description = (meeting.description || '').toLowerCase();
    
    const positiveWords = ['review', 'planning', 'strategy', 'opportunity', 'success', 'growth'];
    const negativeWords = ['problem', 'issue', 'challenge', 'crisis', 'urgent', 'fire'];
    
    let positiveCount = 0;
    let negativeCount = 0;
    
    const text = title + ' ' + description;
    
    positiveWords.forEach(word => {
      if (text.includes(word)) positiveCount++;
    });
    
    negativeWords.forEach(word => {
      if (text.includes(word)) negativeCount++;
    });
    
    if (positiveCount > negativeCount) return 'positive';
    if (negativeCount > positiveCount) return 'negative';
    return 'neutral';
  }

  assessComplexity(meeting) {
    const description = meeting.description || '';
    const wordCount = description.split(' ').length;
    
    if (wordCount > 100) return 'high';
    if (wordCount > 50) return 'medium';
    return 'low';
  }

  calculatePreparationScore(meeting) {
    let score = 50; // Base score
    
    // Points for detailed description
    if (meeting.description && meeting.description.length > 50) {
      score += 20;
    }
    
    // Points for clear location
    if (meeting.location && meeting.location !== 'TBD') {
      score += 10;
    }
    
    // Points for agenda-like structure
    if (meeting.description && (
        meeting.description.includes('1)') || 
        meeting.description.includes('•') ||
        meeting.description.includes('agenda:'))) {
      score += 20;
    }
    
    return Math.min(100, score);
  }

  generateAISuggestions(meeting) {
    const suggestions = [];
    const type = this.determineMeetingType(meeting);
    
    switch (type) {
      case 'decision':
        suggestions.push('Send pre-read materials 24 hours in advance');
        suggestions.push('Define decision criteria before the meeting');
        suggestions.push('Assign a facilitator to keep discussion focused');
        break;
      case 'brainstorming':
        suggestions.push('Use brainstorming techniques like mind mapping');
        suggestions.push('Set a clear problem statement');
        suggestions.push('Use timer for individual thinking before group discussion');
        break;
      case 'client':
        suggestions.push('Prepare client-specific talking points');
        suggestions.push('Have success metrics ready to discuss');
        suggestions.push('Schedule follow-up in the meeting');
        break;
      case 'training':
        suggestions.push('Provide training materials beforehand');
        suggestions.push('Include interactive exercises');
        suggestions.push('Schedule Q&A session at the end');
        break;
    }
    
    return suggestions;
  }

  async generateDailySummary(meetings) {
    if (!meetings || meetings.length === 0) {
      return {
        totalMeetings: 0,
        totalMinutes: 0,
        averageEfficiency: 0,
        potentialSavings: 0,
        recommendations: []
      };
    }

    let totalMinutes = 0;
    let totalEfficiency = 0;
    let potentialSavings = 0;

    const analyses = await Promise.all(
      meetings.map(meeting => this.analyzeMeeting(meeting))
    );

    analyses.forEach((analysis, index) => {
      const meeting = meetings[index];
      totalMinutes += meeting.duration;
      totalEfficiency += analysis.efficiencyScore;
      
      // Calculate potential savings (inefficient meetings)
      if (analysis.efficiencyScore < this.efficiencyThreshold) {
        const optimalDuration = this.calculateOptimalDuration(meeting);
        potentialSavings += Math.max(0, meeting.duration - optimalDuration);
      }
    });

    const averageEfficiency = Math.round(totalEfficiency / meetings.length);
    
    // Generate recommendations
    const recommendations = [];
    
    if (averageEfficiency < this.efficiencyThreshold) {
      recommendations.push('Overall meeting efficiency is below target. Consider reviewing meeting formats.');
    }
    
    if (potentialSavings > 60) {
      recommendations.push(`Potential to save ${potentialSavings} minutes (${Math.round(potentialSavings/60)} hours) by optimizing meetings`);
    }
    
    const longMeetings = meetings.filter(m => m.duration > 60);
    if (longMeetings.length > 0) {
      recommendations.push(`Consider breaking ${longMeetings.length} long meeting(s) into shorter sessions`);
    }

    return {
      totalMeetings: meetings.length,
      totalMinutes,
      averageEfficiency,
      potentialSavings: Math.round(potentialSavings),
      recommendations
    };
  }
}

module.exports = Analyzer;