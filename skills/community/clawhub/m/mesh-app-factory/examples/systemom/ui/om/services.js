export default {
inject:['service', 'tags'],
data() {return {
    services:[],
    cdns:[],
    serviceNum:0,
    search:'',
    install:{service:'',addr:'',dlg:false,start:0,end:32768},
    page:{cur:1, max:0}
}},
created(){
    var cur=this.service.getRt("cur", 1);
    this.page.cur=cur;
    this.query_services(cur);
},
methods:{
service_detail(sn) {
    this.service.go_to('/om/servicedetail?service='+sn);
},
query_services(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/service/list?offset="+offset+"&num="+this.service.N_PAGE};
    this.service.request_private(opts, "company").then(resp=>{
        if(resp.code != RetCode.OK) {
            console.warn("request failed:" + resp.code + ",info:" + resp.info);
            this.services=[];
            this.page.max=0;
            this.page.cur=1;
            return;
        }
        this.service.setRt("cur", pg);
        this.fmt_services(resp.data);
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
search_service() {
    if(this.search=='') {
        this.query_services(1);
        return;
    }
    var opts={method:"GET", url:"/service/list?search="+this.search};
    this.service.request_private(opts, "company").then(resp=>{
        if(resp.code != RetCode.OK) {
            console.warn("request failed:" + resp.code + ",info:" + resp.info);
            this.services=[];
            this.page.max=0;
            this.page.cur=1;
            return;
        }
        this.fmt_services(resp.data);
        this.page.max=1;
    })
},
fmt_services(rows) {
    var cols=rows.cols;//service,displayName,author,type,level,version
    var data=rows.services;
    var services=[];
    var row,s;
    for(var i in data) {
        row=data[i];
        s={};
        for(var c in cols) {
            s[cols[c]]=row[c];
        }
        s.icon = '/'+s.service+"/favicon.png";
        s.version=App.intToVer(s.version);
        services.push(s);
    }
    this.services=services;
},
install_service() {
    var dta={service:this.install.service};
    this.service.request_private({method:"POST",url:"/install", data:dta}, "omagent", this.install.addr).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        //设置服务DNS
        var opts={method:"PUT", url:"/om/setPubSrv",
        data:{service:this.install.service, addr:this.install.addr, start:this.install.start, end:this.intall.end}};
        this.service.request_om(opts, "httpdns").then(resp=>{
            this.install.dlg=false;
            this.install.service="";
            this.services=[]; //刷新服务列表
            this.query_services(1);
        });
    })
}
},  
template: `
<q-layout view="hHh lpr fFf">
 <q-header class="bg-grey-1 text-primary">
  <q-toolbar>
   <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
   <q-toolbar-title>{{tags.om.serviceMng}}</q-toolbar-title>
  </q-toolbar>
 </q-header>
 <q-footer class="bg-white q-pa-md">
  <q-input v-model="search" :placeholder="tags.search" dense @keyup.enter="search_service" outlined>
   <template v-slot:append>
    <q-icon v-if="search!==''" name="close" @click="search='';query_services(1)" class="cursor-pointer"></q-icon>
    <q-icon name="search" @click="search_service"></q-icon>
   </template>
   <template v-slot:after>
    <q-btn round color="primary" icon="add_circle" @click="install.dlg=true"></q-btn>
   </template>
  </q-input>
 </q-footer>
 
 <q-page-container>
  <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination v-model="page.cur" color="primary" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_services"></q-pagination>
</div>
<q-list separator>
 <q-item clickable v-ripple v-for="s in services" @click="service_detail(s.service)">
  <q-item-section avatar top>
    <q-avatar square><img :src="s.icon" style="max-height:2em"></q-avatar>
  </q-item-section>
  <q-item-section>
    <q-item-label lines="1">{{s.displayName}}/{{s.service}}</q-item-label>
    <q-item-label caption>{{s.author}}</q-item-label>
  </q-item-section>
  <q-item-section side>{{s.version}}</q-item-section>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="install.dlg"> <!-- 在实例上安装服务 -->
  <q-card style="min-width:62vw;max-width:80vw">
    <q-card-section>
      <div class="text-h6">{{tags.service.install}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <q-input v-model="install.service" :label="tags.service.name"></q-input>
      <q-input v-model="install.addr" :label="tags.dns.addr"></q-input>
      <q-input v-model="install.start" :label="tags.dns.start"></q-input>
      <q-input v-model="install.end" :label="tags.dns.end"></q-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn color="primary" :label="tags.ok" @click="install_service"></q-btn>
      <q-btn color="primary" flat :label="tags.cancel" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<component-alert-dialog :title="tags.alert" :errMsgs="tags.errMsgs"
 :close="tags.close" ref="alertDlg"></component-alert-dialog>
`}