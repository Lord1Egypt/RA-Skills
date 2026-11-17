export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    contacts:[], //联系人列表，包括自己可见的
    details:{},
    detail:{},
    touchlogs:[],
    detailDlg:false,
    search:'',
    newTouchlog:{contact:0,comment:''},
    page:{cur:1,max:0},
    onlyMine:true
}},
created(){
    this.page.cur=this.ibf.getRt("cur",1);
    this.onlyMine=this.ibf.getRt('onlyMine','false') == 'true';
    this.query_contacts(this.page.cur);
},
methods:{
fmt_contact_lines(cols, lines) {
    var contacts=[];
    var dt=new Date();
    var o;
    for(var ln of lines) { //id,name,post,createAt,creator,cname,cid
        o={};
        for(var j in cols) {
            o[cols[j]]=ln[j];
        }
        dt.setTime(o.createAt*60000);
        o.createAt=date2str(dt);
        contacts.push(o);
    }
    this.contacts=contacts;
},
query_contacts(pg) {
    this.ibf.setRt("cur", pg);
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    this.search='';
    var url = this.onlyMine ? "/api/contact/my" : "/api/contact/readable";
    url+="?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK||resp.data.total==0) {
            this.contacts=[];
            this.page={max:0,cur:1};
            return;
        }
        this.fmt_contact_lines(resp.data.cols, resp.data.contacts);
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
search_contacts() {
    if(this.search=='') {
        this.query_contacts(1);
        return;
    }
    var url="/api/contact/search?s="+this.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.fmt_contact_lines(resp.data.cols, resp.data.contacts);
        this.page.max=1;
    })
},
query_touchlogs(id) {
    var url="/api/touchlog/list?contact="+id+"&offset=0&num=5";
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.touchlogs=[];
            return;
        }
        var logs=[];
        var dt=new Date();
        for(var l of resp.data.touchlogs) {
            dt.setTime(l.createAt*60000);
            logs.push({creator:l.creator,comment:l.comment,createAt:date2str(dt)});
        }
        this.touchlogs=logs;
    })
},
show_detail(id) {
    this.newTouchlog={contact:id,comment:''};
    var detail=this.details[id];
    if(!detail) {
        var url="/api/contact/detail?id="+id;
        request({method:"GET",url:url}, this.service.name).then(resp=>{
            if(resp.code!=0) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
                return;
            }
            var dayNum=parseInt(resp.data.birthday);
            if(dayNum>-60000 && dayNum<60000) {
                var birthDate=new Date(dayNum*86400000);
                resp.data.birthday=date2str(birthDate);
                resp.data.age=new Date().getFullYear() - birthDate.getFullYear();
            } else {
                resp.data.birthday=this.tags.unknown;
                resp.data.age=this.tags.unknown;
            }
            this.details[id]=resp.data;
            this.detail=resp.data;
            this.detailDlg=true;
        })
    } else {
        this.detail=detail;
        this.detailDlg=true;
    }
    this.touchlogs=[];
    this.query_touchlogs(id);
},
add_touchlog(){
    var opts={method:"POST",url:"/api/touchlog/add",data:this.newTouchlog};
    request(opts, this.service.name).then(resp=>{
        if(resp.code==0) {
            this.query_touchlogs(this.newTouchlog.contact);
            this.newTouchlog.comment='';
        }
    })
},
onlyMineClk() {
    this.ibf.setRt('onlyMine',this.onlyMine);
    this.page.cur=1;
    this.query_contacts(1);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.home.contacts}}</q-toolbar-title>
    <q-btn flat round dense icon="menu">
      <q-menu>
       <q-list style="min-width:100px">
        <q-item clickable v-close-popup>
          <q-item-section avatar>
           <q-checkbox v-model="onlyMine" @update:model-value="onlyMineClk"></q-checkbox>
          </q-item-section>
          <q-item-section>{{tags.onlyMine}}</q-item-section>
        </q-item>        
        <q-item clickable v-close-popup>
          <q-item-section avatar><q-icon name="file_download"></q-icon></q-item-section>
          <q-item-section>{{tags.menu.export}} eMail</q-item-section>
        </q-item>
       </q-list>
     </q-menu>
   </q-btn>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="search" :label="tags.search" dense @keyup.enter="search_contacts">
    <template v-slot:append>
      <q-icon v-if="search!==''" name="close" @click="query_contacts(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="search_contacts"></q-icon>
    </template>
    </q-input>
  </q-footer>

  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
  <q-pagination color="primary" v-model="page.cur" :max="page.max" max-pages="10"
   boundary-numbers="false" @update:model-value="query_contacts" dense></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.contact.cname}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.contact.name}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.contact.post}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="c in contacts" clickable>
  <q-item-section @click.stop="service.goto('/customer?id='+c.cid)">{{c.cname}}</q-item-section>
  <q-item-section @click.stop="service.goto('/contact?id='+c.id)" no-wrap>
   <q-item-label>{{c.name}}<q-icon :name="tags.sexImg[c.sex]" :color="c.sex==0?'primary':'red'" size="1em"></q-icon></q-item-label>
   <q-item-label caption>{{c.creator}}@{{c.createAt}}</q-item-label>
  </q-item-section>
  <q-item-section @click="show_detail(c.id)">
   <q-item-label caption>{{c.post}}</q-item-label>
   <q-item-label><q-icon name="star" color="yellow" v-for="i in c.level" size="xs"></q-icon></q-item-label>
  </q-item-section>
 </q-item>
</q-list>

    </q-page>
  </q-page-container>
</q-layout>

<!-- 告警弹窗 -->
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>

<!-- 联系人详情弹窗 -->
<q-dialog v-model="detailDlg" position="right">
  <q-card style="min-width:62vw;max-width:80vw">
  <q-card-section>
   <div class="column">
    <div class="col text-subtitle1">
     <q-icon :name="tags.icons['customer']" size="1em" color="primary"></q-icon>&nbsp;{{detail.cname}}
    </div>
    <div class="col self-center no-wrap text-h6">  
      {{detail.name}}&nbsp;{{detail.post}}
      <q-icon :name="tags.sexImg[detail.sex]" :color="detail.sex==0?'primary':'red'" size="1.5em"></q-icon>
    </div>
    <div class="col self-center"> 
      <q-rating v-model="detail.level" disable max="5" size="sm" color="yellow" color-selected="orange"></q-rating>
    </div>
    <div class="col self-center">  
      {{detail.birthday}}({{detail.age}}{{tags.yearsOld}})
    </div>
    <div class="col self-end text-subtitle1">
     <q-icon name="phone" size="1em" color="primary"></q-icon>&nbsp;{{detail.phone}}
    </div>
    <div class="col self-end text-subtitle1">
     <q-icon name="place" size="1em" color="primary"></q-icon>&nbsp;{{detail.address}}
    </div>
   </div>
  </q-card-section>
  <q-card-section>
      <q-separator></q-separator>
    <q-list dense>
      <q-item v-for="t in touchlogs">
        <q-item-section side>{{t.creator}}</q-item-section>
        <q-item-section>{{t.comment}}</q-item-section>
        <q-item-section side>{{t.createAt}}</q-item-section>
      </q-item>
    </q-list>
    <q-list>
      <q-item>
        <q-item-section>
         <q-input :label="tags.touchCtnt" v-model="newTouchlog.comment" type="textarea"
          dense autogrow></q-input>
        </q-item-section>
        <q-item-section avatar><q-icon name="add_circle" color="primary" @click="add_touchlog"></q-icon></q-item-section>
      </q-item>
    </q-list>
  </q-card-section>
  </q-card>
</q-dialog>
`
}