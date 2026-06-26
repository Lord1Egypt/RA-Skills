export interface CalendarCategory {
  id: string;
  label: string;
  color: string;
  description?: string;
}

export interface CalendarEvent {
  id: string;
  externalId: string;
  updatedAt: string;
  title: string;
  start: string;
  end: string;
  allDay: boolean;
  category: string;
  completed: boolean;
  notes?: string;
  location?: string;
  color?: string;
  googleEventIds?: Record<string, string>;
}

export interface CalendarFrontmatter {
  version: number;
  title: string;
  timezone: string;
  updatedAt: string;
  categories: CalendarCategory[];
}

export interface CalendarDocument {
  frontmatter: CalendarFrontmatter;
  events: CalendarEvent[];
}
