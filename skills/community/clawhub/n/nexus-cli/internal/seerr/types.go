package seerr

// RequestPage represents a paginated Seerr request response.
type RequestPage struct {
	PageInfo struct {
		Results int `json:"results"`
	} `json:"pageInfo"`
	Results []Request `json:"results"`
}

// Request represents a Seerr media request.
type Request struct {
	ID     int  `json:"id"`
	Status int  `json:"status"`
	Type   string `json:"type"`
	Is4K   bool `json:"is4k"`
	Media  struct {
		MediaType string `json:"mediaType"`
		TmdbID    int    `json:"tmdbId"`
	} `json:"media"`
	CreatedAt   string `json:"createdAt"`
	RequestedBy struct {
		DisplayName string `json:"displayName"`
	} `json:"requestedBy"`
}
