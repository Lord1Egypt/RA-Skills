export default {
inject:['service', 'tags'],
data() {return {
    nodes:[],
    page:{cur:1, max:0}
}},
created() {
    var cur=this.service.getRt("cur", 1);
    this.page.cur=cur;
    this.fetch_services(cur);
},
methods:{
service_detail(sn) {
    this.service.go_to('/om/servicedetail?service='+sn);
},
fetch_services(pg) {
    this.service.setRt("cur", pg);
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url="/status/srvlist?offset="+offset+"&num="+this.service.N_PAGE;
    this.service.request_private({method:"GET",url:url}, "bios").then(resp=>{
        if(resp.code != RetCode.OK) {
            console.warn("request failed:" + resp.code + ",info:" + resp.info);
            this.page.max=0;
            this.nodes=[];
            return;
        }
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
        this.nodes=resp.data.list.map(n=>{
            var v=n.ver;
            n.ver=Math.floor(v/1000000)+'.'+(Math.floor(v/1000)%1000)+'.'+(v%1000);
            return n;
        });//service,partId,addr,status,ver
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
 <q-header class="bg-grey-1 text-primary">
  <q-toolbar>
   <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
   <q-toolbar-title>{{tags.om.srvNodes}}</q-toolbar-title>
  </q-toolbar>
 </q-header>

 <q-page-container>
  <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination v-model="page.cur" color="primary" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="fetch_services"></q-pagination>
</div>
<q-list separator style="max-width:98vw;">
  <q-item>
   <q-item-section>{{tags.om.service}}</q-item-section>
   <q-item-section>{{tags.om.addr}}</q-item-section>
  </q-item>
  <q-item clickable v-ripple v-for="n in nodes" @click="service_detail(n.service)">
   <q-item-section>
    <q-item-label>{{n.addr}}</q-item-label>
    <q-item-label caption>{{n.service}}</q-item-label>
    <q-item-label caption>{{tags.om.ver}}:{{n.ver}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{tags.om.status}}:{{n.status}}</q-item-label>
    <q-item-label>{{tags.om.partId}}:{{n.partId}}</q-item-label>
   </q-item-section>
  </q-item>
</q-list>
  </q-page>
 </q-page-container>
</q-layout>
`
}