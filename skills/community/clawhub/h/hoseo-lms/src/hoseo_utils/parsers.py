from html.parser import HTMLParser


class TokenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.logintoken = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "input" and attrs_dict.get("name") == "logintoken":
            self.logintoken = attrs_dict.get("value")


class CourseListParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.courses = []
        self.in_name_cell = False
        self.in_prof_cell = False
        self.current_link = None
        self.current_title = ""
        self.current_prof = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "")

        if tag == "td" and "col-name" in classes:
            self.in_name_cell = True
        elif tag == "td" and "col-professor" in classes:
            self.in_prof_cell = True

        if tag == "a" and self.in_name_cell:
            href = attrs_dict.get("href", "")
            if "course/view.php" in href:
                self.current_link = href

    def handle_data(self, data):
        if self.in_name_cell and self.current_link:
            self.current_title += data.strip()
        if self.in_prof_cell:
            self.current_prof += data.strip()

    def handle_endtag(self, tag):
        if tag == "td":
            self.in_name_cell = False
            self.in_prof_cell = False

        if tag == "tr":
            if self.current_link and self.current_title:
                if not any(c["url"] == self.current_link for c in self.courses):
                    self.courses.append(
                        {
                            "url": self.current_link,
                            "title": self.current_title.strip(),
                            "professor": self.current_prof.strip(),
                        }
                    )
            self.current_link = None
            self.current_title = ""
            self.current_prof = ""


class ActivityParser(HTMLParser):
    ACTIVITY_TYPE_MAP = {
        "vod": "vod",
        "assign": "assign",
        "quiz": "quiz",
        "ubboard": "board",
        "forum": "board",
    }

    def __init__(self):
        super().__init__()
        self.activities = []
        self.in_activity_li = False
        self.in_instancename = False
        self.current_name = ""
        self.current_type = "other"
        self.current_url = ""

    def _resolve_activity_type(self, classes: str) -> str:
        for keyword, activity_type in self.ACTIVITY_TYPE_MAP.items():
            if keyword in classes:
                return activity_type
        return "other"

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "")

        if tag == "li" and "activity" in classes:
            self.in_activity_li = True
            self.current_name = ""
            self.current_url = ""
            self.current_type = self._resolve_activity_type(classes)

        if self.in_activity_li and tag == "a":
            self.current_url = attrs_dict.get("href", "")

        if self.in_activity_li and tag == "span" and "instancename" in classes:
            self.in_instancename = True

    def handle_data(self, data):
        if self.in_instancename:
            self.current_name += data

    def handle_endtag(self, tag):
        if tag == "span" and self.in_instancename:
            self.in_instancename = False

        if tag == "li" and self.in_activity_li:
            name = self.current_name.replace("\n", " ").strip()
            if name:
                self.activities.append(
                    {
                        "type": self.current_type,
                        "name": name,
                        "url": self.current_url,
                    }
                )
            self.in_activity_li = False
            self.current_name = ""
            self.current_type = "other"
            self.current_url = ""


class FirstTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.table_count = 0
        self.in_row = False
        self.in_cell = False
        self.current_cell = ""
        self.current_row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table_count += 1
            if self.table_count == 1:
                self.in_table = True
        elif tag == "tr" and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th") and self.in_row:
            self.in_cell = True
            self.current_cell = ""

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data.strip() + " "

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.in_cell:
            self.current_row.append(self.current_cell.strip())
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            if any(self.current_row):
                self.rows.append(self.current_row)
            self.current_row = []
            self.in_row = False
        elif tag == "table" and self.in_table:
            self.in_table = False

